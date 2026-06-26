#!/usr/bin/env python3
"""
Kubernetes DevOps Toolkit - Core Module

This module provides comprehensive tools for managing Kubernetes clusters,
deployments, monitoring, and troubleshooting.
"""

from typing import List, Dict, Optional, Any
from pathlib import Path
import yaml
import json
from datetime import datetime
from dataclasses import dataclass

try:
    from kubernetes import client, config, watch
    from kubernetes.client.exceptions import ApiException
except ImportError:
    pass


@dataclass
class PodInfo:
    """Pod information container"""
    name: str
    namespace: str
    status: str
    ready: str
    restarts: int
    age: str
    node: str
    ip: str


@dataclass
class NodeInfo:
    """Node information container"""
    name: str
    status: str
    roles: List[str]
    age: str
    version: str
    internal_ip: str
    os_image: str
    cpu_capacity: str
    memory_capacity: str


class K8sManager:
    """
    Main Kubernetes cluster management class.
    
    Provides unified interface for:
    - Cluster connection and context management
    - Resource operations (Pods, Deployments, Services)
    - Monitoring and logging
    - Troubleshooting and diagnostics
    """
    
    def __init__(self, kubeconfig_path: Optional[str] = None, context: Optional[str] = None):
        """
        Initialize K8sManager.
        
        Args:
            kubeconfig_path: Path to kubeconfig file (default: ~/.kube/config)
            context: Kubernetes context to use (default: current context)
        """
        self.kubeconfig_path = kubeconfig_path or "~/.kube/config"
        self.context = context
        self._connected = False
        self._core_v1 = None
        self._apps_v1 = None
        self._networking_v1 = None
        
    def connect(self) -> bool:
        """
        Establish connection to Kubernetes cluster.
        
        Returns:
            bool: True if connection successful
        """
        try:
            config.load_kube_config(
                config_file=self.kubeconfig_path,
                context=self.context
            )
            self._core_v1 = client.CoreV1Api()
            self._apps_v1 = client.AppsV1Api()
            self._networking_v1 = client.NetworkingV1Api()
            self._connected = True
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            return False
    
    def is_connected(self) -> bool:
        """Check if connected to cluster"""
        return self._connected
    
    def list_contexts(self) -> List[Dict[str, str]]:
        """
        List all available contexts in kubeconfig.
        
        Returns:
            List of context dictionaries
        """
        contexts, current = config.list_kube_config_contexts(
            config_file=self.kubeconfig_path
        )
        return [
            {
                "name": ctx["name"],
                "cluster": ctx.get("context", {}).get("cluster", ""),
                "user": ctx.get("context", {}).get("user", ""),
                "current": ctx["name"] == current["name"] if current else False
            }
            for ctx in contexts
        ]
    
    def switch_context(self, context_name: str) -> bool:
        """
        Switch to a different context.
        
        Args:
            context_name: Name of the context to switch to
            
        Returns:
            bool: True if switch successful
        """
        self.context = context_name
        return self.connect()
    
    def get_cluster_version(self) -> str:
        """
        Get Kubernetes cluster version.
        
        Returns:
            Version string
        """
        if not self._connected:
            raise RuntimeError("Not connected to cluster")
        
        version = client.VersionApi().get_code()
        return f"{version.major}.{version.minor}"
    
    def get_nodes(self) -> List[NodeInfo]:
        """
        Get list of all nodes in the cluster.
        
        Returns:
            List of NodeInfo objects
        """
        if not self._connected:
            raise RuntimeError("Not connected to cluster")
        
        nodes = self._core_v1.list_node()
        result = []
        
        for node in nodes.items:
            roles = []
            if "node-role.kubernetes.io/control-plane" in node.metadata.labels:
                roles.append("control-plane")
            if "node-role.kubernetes.io/worker" in node.metadata.labels:
                roles.append("worker")
            
            internal_ip = ""
            for addr in node.status.addresses:
                if addr.type == "InternalIP":
                    internal_ip = addr.address
                    break
            
            cpu = node.status.capacity.get("cpu", "N/A")
            memory = node.status.capacity.get("memory", "N/A")
            
            result.append(NodeInfo(
                name=node.metadata.name,
                status="Ready" if any(
                    c.status == "True" and c.type == "Ready"
                    for c in node.status.conditions
                ) else "NotReady",
                roles=roles or ["worker"],
                age=self._calculate_age(node.metadata.creation_timestamp),
                version=node.status.node_info.kubelet_version,
                internal_ip=internal_ip,
                os_image=node.status.node_info.os_image,
                cpu_capacity=cpu,
                memory_capacity=memory
            ))
        
        return result
    
    def get_pods(self, namespace: str = "default", 
                 label_selector: Optional[str] = None) -> List[PodInfo]:
        """
        Get list of pods in a namespace.
        
        Args:
            namespace: Namespace to query
            label_selector: Label selector filter
            
        Returns:
            List of PodInfo objects
        """
        if not self._connected:
            raise RuntimeError("Not connected to cluster")
        
        pods = self._core_v1.list_namespaced_pod(
            namespace=namespace,
            label_selector=label_selector
        )
        
        result = []
        for pod in pods.items:
            restarts = 0
            ready = "0/0"
            
            if pod.status.container_statuses:
                ready_count = sum(
                    1 for c in pod.status.container_statuses if c.ready
                )
                total = len(pod.status.container_statuses)
                ready = f"{ready_count}/{total}"
                restarts = sum(
                    c.restart_count for c in pod.status.container_statuses
                )
            
            result.append(PodInfo(
                name=pod.metadata.name,
                namespace=pod.metadata.namespace,
                status=pod.status.phase,
                ready=ready,
                restarts=restarts,
                age=self._calculate_age(pod.metadata.creation_timestamp),
                node=pod.spec.node_name or "N/A",
                ip=pod.status.pod_ip or "N/A"
            ))
        
        return result
    
    def get_pod_logs(self, pod_name: str, namespace: str = "default",
                     container: Optional[str] = None, tail_lines: int = 100) -> str:
        """
        Get logs from a pod.
        
        Args:
            pod_name: Name of the pod
            namespace: Pod namespace
            container: Container name (for multi-container pods)
            tail_lines: Number of lines to return
            
        Returns:
            Log content
        """
        if not self._connected:
            raise RuntimeError("Not connected to cluster")
        
        try:
            logs = self._core_v1.read_namespaced_pod_log(
                name=pod_name,
                namespace=namespace,
                container=container,
                tail_lines=tail_lines
            )
            return logs
        except ApiException as e:
            return f"Error fetching logs: {e}"
    
    def diagnose_pod(self, pod_name: str, namespace: str = "default") -> Dict[str, Any]:
        """
        Run diagnostics on a pod and provide troubleshooting suggestions.
        
        Args:
            pod_name: Name of the pod
            namespace: Pod namespace
            
        Returns:
            Diagnosis report dictionary
        """
        if not self._connected:
            raise RuntimeError("Not connected to cluster")
        
        try:
            pod = self._core_v1.read_namespaced_pod(pod_name, namespace)
        except ApiException as e:
            return {"status": "error", "message": f"Pod not found: {e}"}
        
        issues = []
        suggestions = []
        
        # Check pod status
        if pod.status.phase == "Pending":
            issues.append("Pod is in Pending state")
            
            # Check events for scheduling issues
            events = self._core_v1.list_namespaced_event(
                namespace=namespace,
                field_selector=f"involvedObject.name={pod_name}"
            )
            for event in events.items:
                if event.type == "Warning":
                    issues.append(f"Event: {event.reason} - {event.message}")
                    if "Insufficient" in event.message:
                        suggestions.append("Consider scaling cluster or reducing resource requests")
                    if "PersistentVolumeClaim" in event.message:
                        suggestions.append("Check PVC binding status and storage class")
        
        elif pod.status.phase == "Failed":
            issues.append("Pod has failed")
            suggestions.append("Check container exit code and logs")
            suggestions.append("Verify image exists and is accessible")
        
        elif pod.status.phase == "CrashLoopBackOff":
            issues.append("Pod is in CrashLoopBackOff")
            suggestions.append("Check application logs for errors")
            suggestions.append("Verify startup probes and health checks")
            suggestions.append("Check resource limits (OOMKilled?)")
        
        # Check container statuses
        if pod.status.container_statuses:
            for container in pod.status.container_statuses:
                if container.state.waiting:
                    issues.append(f"Container {container.name} is waiting: {container.state.waiting.reason}")
                    if container.state.waiting.reason == "ImagePullBackOff":
                        suggestions.append(f"Check image name/tag for container {container.name}")
                        suggestions.append("Verify image registry credentials")
                
                if container.state.terminated:
                    if container.state.terminated.exit_code != 0:
                        issues.append(f"Container {container.name} exited with code {container.state.terminated.exit_code}")
                        if container.state.terminated.reason == "OOMKilled":
                            suggestions.append(f"Increase memory limit for container {container.name}")
        
        return {
            "pod_name": pod_name,
            "namespace": namespace,
            "phase": pod.status.phase,
            "issues": issues,
            "suggestions": suggestions,
            "logs_preview": self.get_pod_logs(pod_name, namespace, tail_lines=50)
        }
    
    def get_events(self, namespace: Optional[str] = None, 
                   field_selector: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get cluster events.
        
        Args:
            namespace: Namespace (None for all namespaces)
            field_selector: Field selector filter
            
        Returns:
            List of event dictionaries
        """
        if not self._connected:
            raise RuntimeError("Not connected to cluster")
        
        if namespace:
            events = self._core_v1.list_namespaced_event(
                namespace=namespace,
                field_selector=field_selector
            )
        else:
            events = self._core_v1.list_event_for_all_namespaces(
                field_selector=field_selector
            )
        
        return [
            {
                "type": event.type,
                "reason": event.reason,
                "message": event.message,
                "namespace": event.metadata.namespace,
                "involved_object": event.involved_object.name,
                "count": event.count,
                "last_seen": event.last_timestamp.isoformat() if event.last_timestamp else None
            }
            for event in events.items
        ]
    
    def _calculate_age(self, timestamp) -> str:
        """Calculate human-readable age from timestamp"""
        if not timestamp:
            return "Unknown"
        
        now = datetime.now(timestamp.tzinfo)
        delta = now - timestamp
        
        days = delta.days
        hours = delta.seconds // 3600
        minutes = (delta.seconds % 3600) // 60
        
        if days > 0:
            return f"{days}d"
        elif hours > 0:
            return f"{hours}h"
        else:
            return f"{minutes}m"


class HelmManager:
    """
    Helm chart management wrapper.
    
    Provides simplified interface for common Helm operations.
    """
    
    def __init__(self, kubeconfig_path: Optional[str] = None):
        self.kubeconfig_path = kubeconfig_path or "~/.kube/config"
    
    def install(self, release_name: str, chart: str, namespace: str = "default",
                values: Optional[Dict[str, Any]] = None, version: Optional[str] = None) -> bool:
        """
        Install a Helm chart.
        
        Args:
            release_name: Name for the release
            chart: Chart reference (repo/chart or path)
            namespace: Target namespace
            values: Values to override
            version: Chart version
            
        Returns:
            bool: True if installation successful
        """
        # Implementation would use helm CLI or pyhelm
        import subprocess
        
        cmd = ["helm", "install", release_name, chart, "-n", namespace]
        
        if values:
            for key, val in values.items():
                cmd.extend(["--set", f"{key}={val}"])
        
        if version:
            cmd.extend(["--version", version])
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Helm install failed: {e.stderr}")
            return False
    
    def upgrade(self, release_name: str, chart: Optional[str] = None,
                namespace: str = "default", values: Optional[Dict[str, Any]] = None) -> bool:
        """
        Upgrade a Helm release.
        
        Args:
            release_name: Name of the release
            chart: Chart reference (uses existing if not specified)
            namespace: Release namespace
            values: Values to override
            
        Returns:
            bool: True if upgrade successful
        """
        import subprocess
        
        cmd = ["helm", "upgrade", release_name]
        
        if chart:
            cmd.append(chart)
        else:
            cmd.append(release_name)
        
        cmd.extend(["-n", namespace])
        
        if values:
            for key, val in values.items():
                cmd.extend(["--set", f"{key}={val}"])
        
        cmd.append("--install")  # Install if not exists
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Helm upgrade failed: {e.stderr}")
            return False
    
    def rollback(self, release_name: str, revision: int, namespace: str = "default") -> bool:
        """
        Rollback a Helm release to a specific revision.
        
        Args:
            release_name: Name of the release
            revision: Revision number to rollback to
            namespace: Release namespace
            
        Returns:
            bool: True if rollback successful
        """
        import subprocess
        
        cmd = ["helm", "rollback", release_name, str(revision), "-n", namespace]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            print(f"Helm rollback failed: {e.stderr}")
            return False
    
    def list_releases(self, namespace: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List Helm releases.
        
        Args:
            namespace: Filter by namespace (None for all)
            
        Returns:
            List of release dictionaries
        """
        import subprocess
        import json
        
        cmd = ["helm", "list", "-o", "json"]
        
        if namespace:
            cmd.extend(["-n", namespace])
        else:
            cmd.append("--all-namespaces")
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, check=True)
            releases = json.loads(result.stdout)
            return releases
        except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
            print(f"Failed to list releases: {e}")
            return []


if __name__ == "__main__":
    # Example usage
    print("Kubernetes DevOps Toolkit")
    print("=========================")
    print("\nExample usage:")
    print("  from kubernetes_devops_toolkit import K8sManager, HelmManager")
    print("  manager = K8sManager()")
    print("  manager.connect()")
    print("  pods = manager.get_pods('default')")
