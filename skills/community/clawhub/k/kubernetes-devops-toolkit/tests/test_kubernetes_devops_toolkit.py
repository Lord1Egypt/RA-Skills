#!/usr/bin/env python3
"""
Tests for Kubernetes DevOps Toolkit
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from kubernetes_devops_toolkit import K8sManager, HelmManager, PodInfo, NodeInfo


class TestK8sManager:
    """Test cases for K8sManager"""
    
    def test_init_default(self):
        """Test default initialization"""
        manager = K8sManager()
        assert manager.kubeconfig_path == "~/.kube/config"
        assert manager.context is None
        assert not manager.is_connected()
    
    def test_init_custom(self):
        """Test initialization with custom values"""
        manager = K8sManager(
            kubeconfig_path="/custom/config",
            context="production"
        )
        assert manager.kubeconfig_path == "/custom/config"
        assert manager.context == "production"
    
    def test_calculate_age_days(self):
        """Test age calculation for days"""
        from datetime import datetime, timezone
        manager = K8sManager()
        
        # 5 days ago
        timestamp = datetime.now(timezone.utc) - __import__('datetime').timedelta(days=5)
        assert manager._calculate_age(timestamp) == "5d"
    
    def test_calculate_age_hours(self):
        """Test age calculation for hours"""
        from datetime import datetime, timezone
        manager = K8sManager()
        
        # 3 hours ago
        timestamp = datetime.now(timezone.utc) - __import__('datetime').timedelta(hours=3)
        assert manager._calculate_age(timestamp) == "3h"
    
    def test_calculate_age_minutes(self):
        """Test age calculation for minutes"""
        from datetime import datetime, timezone
        manager = K8sManager()
        
        # 30 minutes ago
        timestamp = datetime.now(timezone.utc) - __import__('datetime').timedelta(minutes=30)
        assert manager._calculate_age(timestamp) == "30m"


class TestPodInfo:
    """Test cases for PodInfo dataclass"""
    
    def test_pod_info_creation(self):
        """Test PodInfo creation"""
        pod = PodInfo(
            name="test-pod",
            namespace="default",
            status="Running",
            ready="1/1",
            restarts=0,
            age="5m",
            node="node-1",
            ip="10.0.0.1"
        )
        assert pod.name == "test-pod"
        assert pod.status == "Running"
        assert pod.ready == "1/1"


class TestNodeInfo:
    """Test cases for NodeInfo dataclass"""
    
    def test_node_info_creation(self):
        """Test NodeInfo creation"""
        node = NodeInfo(
            name="worker-1",
            status="Ready",
            roles=["worker"],
            age="30d",
            version="v1.28.0",
            internal_ip="192.168.1.1",
            os_image="Ubuntu 22.04",
            cpu_capacity="4",
            memory_capacity="16Gi"
        )
        assert node.name == "worker-1"
        assert node.status == "Ready"
        assert "worker" in node.roles


class TestHelmManager:
    """Test cases for HelmManager"""
    
    def test_init_default(self):
        """Test default initialization"""
        helm = HelmManager()
        assert helm.kubeconfig_path == "~/.kube/config"
    
    def test_init_custom(self):
        """Test initialization with custom values"""
        helm = HelmManager(kubeconfig_path="/custom/kubeconfig")
        assert helm.kubeconfig_path == "/custom/kubeconfig"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
