#!/usr/bin/env python3
"""
Basic usage example for Kubernetes DevOps Toolkit

This example demonstrates how to use the toolkit for common K8s operations.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from kubernetes_devops_toolkit import K8sManager, HelmManager


def main():
    print("=" * 60)
    print("Kubernetes DevOps Toolkit - Basic Usage Example")
    print("=" * 60)
    
    # Initialize K8s Manager
    print("\n1. Initialize K8s Manager")
    print("-" * 40)
    manager = K8sManager(kubeconfig_path="~/.kube/config")
    print(f"   Kubeconfig: {manager.kubeconfig_path}")
    
    # List available contexts
    print("\n2. List Available Contexts")
    print("-" * 40)
    try:
        contexts = manager.list_contexts()
        for ctx in contexts:
            marker = " (current)" if ctx["current"] else ""
            print(f"   - {ctx['name']}{marker}")
            print(f"     Cluster: {ctx['cluster']}, User: {ctx['user']}")
    except Exception as e:
        print(f"   Note: Could not list contexts - {e}")
    
    # Connect to cluster (will fail without actual K8s)
    print("\n3. Connect to Cluster")
    print("-" * 40)
    connected = manager.connect()
    if connected:
        print("   ✅ Successfully connected to cluster!")
        print(f"   K8s Version: {manager.get_cluster_version()}")
        
        # Get nodes
        print("\n4. List Cluster Nodes")
        print("-" * 40)
        nodes = manager.get_nodes()
        print(f"   Total nodes: {len(nodes)}")
        for node in nodes:
            print(f"   - {node.name}: {node.status} ({', '.join(node.roles)})")
        
        # Get pods
        print("\n5. List Pods in default namespace")
        print("-" * 40)
        pods = manager.get_pods(namespace="default")
        print(f"   Total pods: {len(pods)}")
        for pod in pods[:5]:  # Show first 5
            print(f"   - {pod.name}: {pod.status} (Ready: {pod.ready})")
        
        # Diagnose a pod
        if pods:
            print("\n6. Pod Diagnosis Example")
            print("-" * 40)
            pod = pods[0]
            print(f"   Diagnosing: {pod.name}")
            diagnosis = manager.diagnose_pod(pod.name, "default")
            print(f"   Status: {diagnosis.get('phase', 'Unknown')}")
            if diagnosis.get('issues'):
                print("   Issues found:")
                for issue in diagnosis['issues']:
                    print(f"     - {issue}")
    else:
        print("   ⚠️  Could not connect to cluster (expected in demo)")
        print("   This is normal if you don't have a K8s cluster running.")
    
    # Helm example
    print("\n7. Helm Manager Example")
    print("-" * 40)
    helm = HelmManager()
    print("   HelmManager initialized")
    print("   Available operations:")
    print("     - helm.install(release_name, chart, namespace)")
    print("     - helm.upgrade(release_name, namespace)")
    print("     - helm.rollback(release_name, revision)")
    print("     - helm.list_releases()")
    
    print("\n" + "=" * 60)
    print("Example completed!")
    print("=" * 60)
    print("\nFor more information, see README.md")


if __name__ == "__main__":
    main()
