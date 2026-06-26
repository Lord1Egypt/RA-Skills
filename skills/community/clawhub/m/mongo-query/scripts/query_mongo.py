#!/usr/bin/env python3
"""
MongoDB Query Script

Query MongoDB databases using pymongo (no mongo binary required).
Supports both direct IP connection and Kubernetes port-forward.

Usage:
    python query_mongo.py --uri "mongodb://user:pass@host:port/?options" --list-dbs
    python query_mongo.py --uri "mongodb://user:pass@host:port/?options" --db <db> --list-collections
    python query_mongo.py --uri "mongodb://user:pass@host:port/?options" --db <db> --collection <col> --query '{"key": "value"}'

Dependencies:
    pip install pymongo
"""

import argparse
import json
import re
import sys
import subprocess
import time
import signal
import os
from urllib.parse import urlparse, parse_qs

try:
    from pymongo import MongoClient
    from pymongo.errors import PyMongoError
except ImportError:
    print("Error: pymongo is required. Install it with: pip install pymongo", file=sys.stderr)
    sys.exit(1)

# Global variable to track port-forward process
port_forward_process = None

def is_ip_address(addr):
    """Check if the address is an IP address (IPv4 or IPv6)."""
    # Remove port if present
    host = addr.split(':')[0] if ':' in addr else addr
    
    # IPv4 pattern
    ipv4_pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if re.match(ipv4_pattern, host):
        return True
    
    # IPv6 pattern (simplified)
    ipv6_pattern = r'^[0-9a-fA-F:]+$'
    if re.match(ipv6_pattern, host) and host.count(':') >= 2:
        return True
    
    # localhost
    if host in ['localhost', '127.0.0.1', '::1']:
        return True
    
    return False

def parse_mongo_uri(uri):
    """Parse MongoDB URI and extract connection details."""
    try:
        parsed = urlparse(uri)
        
        # Extract host and port
        host = parsed.hostname or 'localhost'
        port = parsed.port or 27017
        
        # Extract username and password
        username = parsed.username or ''
        password = parsed.password or ''
        
        # Extract query options
        options = {}
        if parsed.query:
            options = {k: v[0] for k, v in parse_qs(parsed.query).items()}
        
        # Extract database name from path
        database = parsed.path.lstrip('/') if parsed.path else None
        
        return {
            'host': host,
            'port': port,
            'username': username,
            'password': password,
            'options': options,
            'database': database,
            'original_uri': uri
        }
    except Exception as e:
        print(f"Error parsing MongoDB URI: {e}", file=sys.stderr)
        sys.exit(1)

def start_port_forward(service_name, namespace, local_port=27017):
    """Start kubectl port-forward to MongoDB service."""
    global port_forward_process
    
    # Extract service name from address if it includes port
    if ':' in service_name:
        service_host = service_name.split(':')[0]
        service_port = service_name.split(':')[1]
    else:
        service_host = service_name
        service_port = '27017'
    
    # Determine if it's a full service name or just a service name
    if '.' in service_host and 'svc' in service_host:
        # Full service name like mongodb.mongodb.svc.cluster.local
        # Extract namespace from service name
        parts = service_host.split('.')
        if len(parts) >= 2:
            svc_name = parts[0]
            target_namespace = parts[1]
        else:
            svc_name = service_host
            target_namespace = namespace
    else:
        # Just service name
        svc_name = service_host
        target_namespace = namespace
    
    cmd = [
        'kubectl', 'port-forward',
        f'svc/{svc_name}',
        f'{local_port}:{service_port}',
        '-n', target_namespace
    ]
    
    print(f"Starting port-forward: {' '.join(cmd)}", file=sys.stderr)
    
    try:
        port_forward_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            preexec_fn=os.setsid
        )
        
        # Wait a bit for port-forward to establish
        time.sleep(2)
        
        if port_forward_process.poll() is not None:
            stderr = port_forward_process.stderr.read().decode('utf-8')
            raise Exception(f"Port-forward failed: {stderr}")
        
        return True
    except Exception as e:
        print(f"Error starting port-forward: {e}", file=sys.stderr)
        return False

def stop_port_forward():
    """Stop the port-forward process."""
    global port_forward_process
    if port_forward_process:
        try:
            os.killpg(os.getpgid(port_forward_process.pid), signal.SIGTERM)
            port_forward_process.wait()
        except Exception as e:
            print(f"Error stopping port-forward: {e}", file=sys.stderr)
        finally:
            port_forward_process = None

def build_local_uri(parsed_uri, local_port=27017):
    """Build MongoDB URI for local connection (after port-forward)."""
    from urllib.parse import quote_plus
    
    username = quote_plus(parsed_uri['username']) if parsed_uri['username'] else ''
    password = quote_plus(parsed_uri['password']) if parsed_uri['password'] else ''
    
    # Build options string
    opts = '&'.join(f"{k}={v}" for k, v in parsed_uri['options'].items()) if parsed_uri['options'] else ''
    
    if username and password:
        uri = f"mongodb://{username}:{password}@localhost:{local_port}/?{opts}"
    else:
        uri = f"mongodb://localhost:{local_port}/?{opts}"
    
    return uri

def get_client(uri):
    """Get MongoDB client connection."""
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        # Test connection
        client.admin.command('ping')
        return client
    except PyMongoError as e:
        print(f"Error connecting to MongoDB: {e}", file=sys.stderr)
        return None

def list_databases(client):
    """List all databases."""
    try:
        dbs = client.list_database_names()
        # Filter out system databases
        return [db for db in dbs if db not in ['admin', 'local', 'config']]
    except PyMongoError as e:
        print(f"Error listing databases: {e}", file=sys.stderr)
        return []

def list_collections(client, db_name):
    """List all collections in a database."""
    try:
        db = client[db_name]
        return db.list_collection_names()
    except PyMongoError as e:
        print(f"Error listing collections: {e}", file=sys.stderr)
        return []

def query_documents(client, db_name, collection, query, limit=10):
    """Execute a query on a collection."""
    try:
        db = client[db_name]
        coll = db[collection]
        cursor = coll.find(query).limit(limit)
        return list(cursor)
    except PyMongoError as e:
        print(f"Error executing query: {e}", file=sys.stderr)
        return []

def format_output(data, raw_json=False):
    """Format output for display."""
    if raw_json:
        return json.dumps(data, indent=2, ensure_ascii=False, default=str)
    
    if isinstance(data, list):
        if len(data) == 0:
            return "No results found."
        
        # Check if it's a list of strings (database names or collection names)
        if all(isinstance(item, str) for item in data):
            return "\n".join(f"- {item}" for item in data)
        
        # Otherwise, it's a list of documents
        output = []
        for i, doc in enumerate(data, 1):
            output.append(f"--- Document {i} ---")
            output.append(json.dumps(doc, indent=2, ensure_ascii=False, default=str))
        return "\n".join(output)
    
    return json.dumps(data, indent=2, ensure_ascii=False, default=str)

def main():
    parser = argparse.ArgumentParser(description='Query MongoDB databases using pymongo')
    parser.add_argument('--uri', required=True,
                        help='MongoDB connection string (e.g., mongodb://user:pass@host:port/?options)')
    parser.add_argument('--list-dbs', action='store_true',
                        help='List all databases')
    parser.add_argument('--db', help='Database name')
    parser.add_argument('--list-collections', action='store_true',
                        help='List collections in the database')
    parser.add_argument('--collection', help='Collection name')
    parser.add_argument('--query', help='MongoDB query in JSON format')
    parser.add_argument('--namespace', default='default',
                        help='Kubernetes namespace for port-forward (required if host is a K8s service name)')
    parser.add_argument('--limit', type=int, default=10,
                        help='Limit number of results (default: 10)')
    parser.add_argument('--json', action='store_true',
                        help='Output raw JSON')
    
    args = parser.parse_args()
    
    # Parse MongoDB URI
    parsed_uri = parse_mongo_uri(args.uri)
    
    # Determine connection method based on host type
    host = parsed_uri['host']
    use_port_forward = not is_ip_address(host)
    
    client = None
    try:
        if use_port_forward:
            print(f"MongoDB host '{host}' is not an IP, using port-forward", file=sys.stderr)
            service_addr = f"{host}:{parsed_uri['port']}"
            if not start_port_forward(service_addr, args.namespace):
                print("Failed to establish port-forward", file=sys.stderr)
                sys.exit(1)
            # Use localhost for connection after port-forward
            mongo_uri = build_local_uri(parsed_uri)
        else:
            # Use original URI for direct connection
            mongo_uri = args.uri
        
        # Connect to MongoDB
        client = get_client(mongo_uri)
        if not client:
            sys.exit(1)
        
        # Execute operations
        if args.list_dbs:
            databases = list_databases(client)
            print(format_output(databases, args.json))
        
        elif args.list_collections:
            if not args.db:
                print("Error: --db is required for listing collections", file=sys.stderr)
                sys.exit(1)
            collections = list_collections(client, args.db)
            print(format_output(collections, args.json))
        
        elif args.query:
            if not args.db or not args.collection:
                print("Error: --db and --collection are required for queries", file=sys.stderr)
                sys.exit(1)
            try:
                query_obj = json.loads(args.query)
            except json.JSONDecodeError as e:
                print(f"Error parsing query JSON: {e}", file=sys.stderr)
                sys.exit(1)
            documents = query_documents(client, args.db, args.collection, query_obj, args.limit)
            print(format_output(documents, args.json))
        
        else:
            parser.print_help()
    
    finally:
        # Close MongoDB connection
        if client:
            client.close()
        # Clean up port-forward
        if use_port_forward:
            stop_port_forward()

if __name__ == '__main__':
    # Register signal handler for clean exit
    signal.signal(signal.SIGINT, lambda s, f: stop_port_forward() or sys.exit(0))
    signal.signal(signal.SIGTERM, lambda s, f: stop_port_forward() or sys.exit(0))
    main()
