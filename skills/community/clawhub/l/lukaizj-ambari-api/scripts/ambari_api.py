#!/usr/bin/env python3
"""
Ambari API Client - Support Ambari 2.7.5 and 3.0.0
Manage Hadoop cluster services via REST API
"""

import argparse
import json
import os
import sys
import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import urljoin
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CONFIG_FILE = os.path.expanduser("~/.claude/skills/ambari-api/config.json")


def load_config():
    """Load cluster configurations from config file"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {"clusters": {}}


def save_config(config):
    """Save cluster configurations to config file"""
    os.makedirs(os.path.dirname(CONFIG_FILE), exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


class AmbariClient:
    """Ambari REST API Client"""

    def __init__(self, base_url, username, password, verify_ssl=False):
        self.base_url = base_url.rstrip('/')
        self.auth = HTTPBasicAuth(username, password)
        self.verify_ssl = verify_ssl
        self.api_base = "/api/v1"
        self.session = requests.Session()
        self.session.headers.update({
            'X-Requested-By': 'ambari',
            'Content-Type': 'application/json'
        })

    def _request(self, method, endpoint, data=None, params=None):
        """Make HTTP request to Ambari API"""
        url = urljoin(self.base_url + self.api_base + '/', endpoint.lstrip('/'))
        try:
            response = self.session.request(
                method=method,
                url=url,
                auth=self.auth,
                json=data,
                params=params,
                verify=self.verify_ssl
            )
            response.raise_for_status()
            if response.content:
                return response.json()
            return {"status": "success"}
        except requests.exceptions.HTTPError as e:
            return {"error": True, "status_code": e.response.status_code,
                    "message": e.response.text}
        except Exception as e:
            return {"error": True, "message": str(e)}

    def get_clusters(self):
        """Get all clusters"""
        result = self._request('GET', 'clusters')
        if 'error' in result:
            return result
        return [c['Clusters']['cluster_name'] for c in result.get('items', [])]

    def get_services(self, cluster):
        """Get all services in a cluster"""
        result = self._request('GET', f'clusters/{cluster}/services',
                               params={'fields': 'ServiceInfo/service_name,ServiceInfo/state'})
        if 'error' in result:
            return result
        services = []
        for s in result.get('items', []):
            service_info = s.get('ServiceInfo', {})
            services.append({
                'service_name': service_info.get('service_name', 'UNKNOWN'),
                'state': service_info.get('state', 'UNKNOWN'),
                'cluster_name': cluster
            })
        return services

    def get_hosts(self, cluster):
        """Get all hosts in a cluster"""
        result = self._request('GET', f'clusters/{cluster}/hosts',
                               params={'fields': 'Hosts/host_name,Hosts/ip,Hosts/host_state'})
        if 'error' in result:
            return result
        hosts = []
        for h in result.get('items', []):
            hosts_info = h.get('Hosts', {})
            hosts.append({
                'host_name': hosts_info.get('host_name', ''),
                'ip': hosts_info.get('ip', ''),
                'state': hosts_info.get('host_state', 'UNKNOWN')
            })
        return hosts

    def get_host_components(self, cluster, host_name):
        """Get all components on a specific host"""
        # Use fields parameter to get service_name and state
        result = self._request('GET', f'clusters/{cluster}/hosts/{host_name}/host_components',
                               params={'fields': 'HostRoles/service_name,HostRoles/state,HostRoles/component_name'})
        if 'error' in result:
            return result
        components = []
        for c in result.get('items', []):
            host_roles = c.get('HostRoles', {})
            components.append({
                'component_name': host_roles.get('component_name', ''),
                'service_name': host_roles.get('service_name', ''),
                'state': host_roles.get('state', 'UNKNOWN')
            })
        return components

    def get_service_info(self, cluster, service_name):
        """Get detailed info about a service"""
        result = self._request('GET', f'clusters/{cluster}/services/{service_name}')
        if 'error' in result:
            return result
        return {
            'service_name': result['ServiceInfo']['service_name'],
            'state': result['ServiceInfo']['state'],
            'cluster_name': cluster
        }

    def service_action(self, cluster, service_name, action):
        """
        Perform action on a service
        Actions: START, STOP, RESTART, INSTALLED (same as STOP)
        """
        valid_actions = ['START', 'STOP', 'RESTART']
        if action.upper() not in valid_actions:
            return {"error": True, "message": f"Invalid action: {action}. Valid: {valid_actions}"}

        endpoint = f'clusters/{cluster}/services/{service_name}'
        data = {'RequestInfo': {'context': f'{action} {service_name}'},
                'Body': {'ServiceInfo': {'state': action.upper()}}}

        return self._request('PUT', endpoint, data=data)

    def component_action(self, cluster, service_name, component_name, host_name, action):
        """
        Perform action on a specific component on a host
        Actions: START, STOP
        Note: STOP sets state to INSTALLED, START sets state to STARTED
        """
        action = action.upper()
        valid_actions = ['START', 'STOP']
        if action not in valid_actions:
            return {"error": True, "message": f"Invalid action: {action}. Valid: {valid_actions}"}

        # Map action to state
        state_map = {'START': 'STARTED', 'STOP': 'INSTALLED'}
        target_state = state_map[action]

        endpoint = f'clusters/{cluster}/hosts/{host_name}/host_components/{component_name}'
        data = {
            'RequestInfo': {'context': f'{action} {component_name} on {host_name}'},
            'Body': {'HostRoles': {'state': target_state}}
        }

        return self._request('PUT', endpoint, data=data)

    def restart_component(self, cluster, service_name, component_name, host_name):
        """Restart a component (stop then start)"""
        # First stop
        stop_result = self.component_action(cluster, service_name, component_name, host_name, 'STOP')
        if 'error' in stop_result and stop_result.get('status_code') != 404:
            return stop_result

        # Then start
        return self.component_action(cluster, service_name, component_name, host_name, 'START')

    def get_request_status(self, cluster, request_id):
        """Get status of an async request"""
        return self._request('GET', f'clusters/{cluster}/requests/{request_id}')


def cmd_config(args):
    """Manage cluster configurations"""
    config = load_config()

    if args.list:
        if not config['clusters']:
            print("No clusters configured. Use 'add' to add a cluster.")
            return
        print("Configured clusters:")
        for name, cfg in config['clusters'].items():
            print(f"  - {name}: {cfg['url']} (user: {cfg['username']})")
        return

    if args.add:
        if not all([args.name, args.url, args.username, args.password]):
            print("Error: --name, --url, --username, and --password required for add")
            sys.exit(1)
        config['clusters'][args.name] = {
            'url': args.url,
            'username': args.username,
            'password': args.password
        }
        save_config(config)
        print(f"Cluster '{args.name}' added successfully.")
        return

    if args.remove:
        if args.name not in config['clusters']:
            print(f"Error: Cluster '{args.name}' not found")
            sys.exit(1)
        del config['clusters'][args.name]
        save_config(config)
        print(f"Cluster '{args.name}' removed.")


def get_client(config_name):
    """Get AmbariClient from config"""
    config = load_config()
    if config_name not in config['clusters']:
        print(f"Error: Cluster '{config_name}' not found in config")
        print("Available clusters:", list(config['clusters'].keys()))
        sys.exit(1)
    cfg = config['clusters'][config_name]
    return AmbariClient(cfg['url'], cfg['username'], cfg['password'])


def cmd_clusters(args):
    """List all clusters"""
    client = get_client(args.config)
    result = client.get_clusters()
    if 'error' in result:
        print("Error:", result['message'])
        sys.exit(1)
    print("Clusters:")
    for c in result:
        print(f"  - {c}")


def cmd_services(args):
    """List or manage services"""
    client = get_client(args.config)

    if args.action:
        result = client.service_action(args.cluster, args.service, args.action)
        if 'error' in result:
            print("Error:", result.get('message', result))
            sys.exit(1)
        print(f"Service '{args.service}' {args.action} request submitted.")
        if 'Requests' in result:
            print(f"Request ID: {result['Requests']['id']}")
    else:
        result = client.get_services(args.cluster)
        if 'error' in result:
            print("Error:", result['message'])
            sys.exit(1)
        print(f"Services in cluster '{args.cluster}':")
        for s in result:
            print(f"  - {s['service_name']}: {s['state']}")


def cmd_hosts(args):
    """List hosts in a cluster"""
    client = get_client(args.config)
    result = client.get_hosts(args.cluster)
    if 'error' in result:
        print("Error:", result['message'])
        sys.exit(1)
    print(f"Hosts in cluster '{args.cluster}':")
    for h in result:
        print(f"  - {h['host_name']}: {h['state']}")


def cmd_components(args):
    """List or manage components on a host"""
    client = get_client(args.config)

    if args.action:
        result = client.component_action(
            args.cluster, args.service, args.component, args.host, args.action
        )
        if 'error' in result:
            print("Error:", result.get('message', result))
            sys.exit(1)
        print(f"Component '{args.component}' {args.action} request submitted on {args.host}.")
        if 'Requests' in result:
            print(f"Request ID: {result['Requests']['id']}")
    else:
        result = client.get_host_components(args.cluster, args.host)
        if 'error' in result:
            print("Error:", result['message'])
            sys.exit(1)
        print(f"Components on host '{args.host}':")
        for c in result:
            print(f"  - {c['component_name']} ({c['service_name']}): {c['state']}")


def cmd_status(args):
    """Get service status"""
    client = get_client(args.config)
    result = client.get_service_info(args.cluster, args.service)
    if 'error' in result:
        print("Error:", result.get('message', result))
        sys.exit(1)
    print(f"Service '{args.service}' in cluster '{args.cluster}':")
    print(f"  State: {result['state']}")


def main():
    parser = argparse.ArgumentParser(
        description='Ambari API Client - Manage Hadoop cluster services'
    )
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Config command
    config_parser = subparsers.add_parser('config', help='Manage cluster configurations')
    config_parser.add_argument('--list', action='store_true', help='List configured clusters')
    config_parser.add_argument('--add', action='store_true', help='Add a cluster config')
    config_parser.add_argument('--remove', action='store_true', help='Remove a cluster config')
    config_parser.add_argument('--name', help='Cluster config name')
    config_parser.add_argument('--url', help='Ambari server URL (e.g., https://ambari:8080)')
    config_parser.add_argument('--username', help='Ambari username')
    config_parser.add_argument('--password', help='Ambari password')
    config_parser.set_defaults(func=cmd_config)

    # Clusters command
    clusters_parser = subparsers.add_parser('clusters', help='List clusters')
    clusters_parser.add_argument('--config', '-c', required=True, help='Cluster config name')
    clusters_parser.set_defaults(func=cmd_clusters)

    # Services command
    services_parser = subparsers.add_parser('services', help='List or manage services')
    services_parser.add_argument('--config', '-c', required=True, help='Cluster config name')
    services_parser.add_argument('--cluster', required=True, help='Cluster name')
    services_parser.add_argument('--service', '-s', help='Service name (for action)')
    services_parser.add_argument('--action', '-a', choices=['START', 'STOP', 'RESTART'],
                                 help='Action to perform')
    services_parser.set_defaults(func=cmd_services)

    # Hosts command
    hosts_parser = subparsers.add_parser('hosts', help='List hosts in a cluster')
    hosts_parser.add_argument('--config', '-c', required=True, help='Cluster config name')
    hosts_parser.add_argument('--cluster', required=True, help='Cluster name')
    hosts_parser.set_defaults(func=cmd_hosts)

    # Components command
    components_parser = subparsers.add_parser('components', help='List or manage components')
    components_parser.add_argument('--config', '-c', required=True, help='Cluster config name')
    components_parser.add_argument('--cluster', required=True, help='Cluster name')
    components_parser.add_argument('--host', help='Host name')
    components_parser.add_argument('--service', '-s', help='Service name')
    components_parser.add_argument('--component', help='Component name')
    components_parser.add_argument('--action', '-a', choices=['START', 'STOP', 'INSTALL'],
                                   help='Action to perform')
    components_parser.set_defaults(func=cmd_components)

    # Status command
    status_parser = subparsers.add_parser('status', help='Get service status')
    status_parser.add_argument('--config', '-c', required=True, help='Cluster config name')
    status_parser.add_argument('--cluster', required=True, help='Cluster name')
    status_parser.add_argument('--service', '-s', required=True, help='Service name')
    status_parser.set_defaults(func=cmd_status)

    args = parser.parse_args()
    if args.command is None:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == '__main__':
    main()