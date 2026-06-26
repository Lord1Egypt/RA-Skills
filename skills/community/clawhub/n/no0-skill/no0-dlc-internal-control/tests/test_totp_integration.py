"""
TOTP Vault + Reference Monitor 集成测试
"""

import asyncio
import os
import pytest
import tempfile
import shutil
from datetime import datetime
from pathlib import Path

# 设置测试环境
os.environ['TOTP_AUTO_APPROVE'] = '1'

from internal_control.totp_vault import (
    TOTPVault,
    MasterKeyManager,
    TOTPKey,
    KeyStatus,
    MFAResult
)
from internal_control.totp_vault.integration import (
    MFAuthorizationProvider,
    ReferenceMonitorWithMFA,
    create_simple_console_callback
)
from internal_control.reference_monitor import (
    AccessOperation,
    AccessDecision,
    DataLevel,
    Agent,
    AgentPermissionLevel,
    AgentAuthenticator
)


class TestTOTPVaultIntegration:
    """TOTP Vault 集成测试"""
    
    @pytest.fixture
    def temp_dir(self):
        """创建临时目录"""
        temp = tempfile.mkdtemp()
        yield temp
        shutil.rmtree(temp)
    
    @pytest.fixture
    def vault(self, temp_dir):
        """创建测试用的 Vault"""
        # 使用临时目录存储密钥
        key_file = Path(temp_dir) / "vault_master.key"
        db_path = Path(temp_dir) / "totp_vault.db"
        
        manager = MasterKeyManager(str(key_file))
        master_key = manager.initialize("test-password")
        
        from internal_control.totp_vault.storage import SQLiteStorage
        storage = SQLiteStorage(str(db_path))
        
        vault = TOTPVault(master_key=master_key, storage=storage)
        return vault
    
    def test_vault_initialization(self, vault):
        """测试 Vault 初始化"""
        assert vault is not None
        assert vault._storage is not None
    
    def test_key_generation(self, vault):
        """测试密钥生成"""
        key_meta = vault.generate_key(context="test_access")
        
        assert key_meta is not None
        assert key_meta.context == "test_access"
        assert key_meta.algorithm == "SHA1"
        assert key_meta.digits == 6
        assert key_meta.interval == 30
        assert key_meta.status == KeyStatus.ACTIVE
    
    def test_key_retrieval(self, vault):
        """测试密钥获取"""
        # 生成密钥
        key_meta = vault.generate_key(context="test_retrieval")
        
        # 通过 ID 获取
        retrieved = vault.get_key_metadata(key_meta.key_id)
        assert retrieved is not None
        assert retrieved.key_id == key_meta.key_id
        
        # 通过上下文获取
        by_context = vault.get_key_by_context("test_retrieval")
        assert by_context is not None
        assert by_context.key_id == key_meta.key_id
    
    def test_totp_computation(self, vault):
        """测试 TOTP 计算"""
        key_meta = vault.generate_key(context="test_totp")
        
        # 计算 TOTP（内部方法）
        totp_code = vault._compute_totp(key_meta.key_id)
        
        assert totp_code is not None
        assert len(totp_code.code) == 6
        assert totp_code.code.isdigit()
        assert totp_code.key_id == key_meta.key_id
        assert totp_code.is_valid()
    
    def test_mfa_flow_success(self, vault):
        """测试 MFA 流程 - 成功场景"""
        key_meta = vault.generate_key(context="test_mfa")
        
        # 创建自动确认的回调
        def auto_approve(request_info):
            return True
        
        result = vault.execute_mfa_flow(key_meta.key_id, auto_approve)
        
        assert result.granted is True
        assert result.key_id == key_meta.key_id
        assert "authorized" in result.message.lower() or "成功" in result.message
    
    def test_mfa_flow_denied(self, vault):
        """测试 MFA 流程 - 拒绝场景"""
        key_meta = vault.generate_key(context="test_mfa_denied")
        
        # 创建拒绝的回调
        def auto_deny(request_info):
            return False
        
        result = vault.execute_mfa_flow(key_meta.key_id, auto_deny)
        
        assert result.granted is False
        assert "declined" in result.message.lower() or "拒绝" in result.message
    
    def test_key_rotation(self, vault):
        """测试密钥轮换"""
        key_meta = vault.generate_key(context="test_rotation")
        original_id = key_meta.key_id
        
        # 轮换密钥
        new_key = vault.rotate_key(key_meta.key_id, grace_period_hours=1)
        
        # 验证新密钥
        assert new_key.key_id == original_id  # ID 保持不变
        assert new_key.status == KeyStatus.ACTIVE
        
        # 验证旧密钥已标记为轮换中
        old_meta = vault.get_key_metadata(original_id)
        # 注意：轮换后元数据会被更新，状态应该是 ACTIVE
        assert old_meta is not None
    
    def test_key_listing(self, vault):
        """测试密钥列表"""
        # 生成多个密钥
        contexts = ["test1", "test2", "test3"]
        for ctx in contexts:
            vault.generate_key(context=ctx)
        
        keys = vault.list_keys()
        assert len(keys) >= len(contexts)
        
        for key in keys:
            assert key.key_id is not None
            assert key.context is not None


class TestMFAAuthorizationProvider:
    """MFA 授权提供者测试"""
    
    @pytest.fixture
    def temp_dir(self):
        temp = tempfile.mkdtemp()
        yield temp
        shutil.rmtree(temp)
    
    @pytest.fixture
    def provider(self, temp_dir):
        """创建测试用的 MFA Provider"""
        key_file = Path(temp_dir) / "vault_master.key"
        db_path = Path(temp_dir) / "totp_vault.db"
        
        manager = MasterKeyManager(str(key_file))
        master_key = manager.initialize("test-password")
        
        from internal_control.totp_vault.storage import SQLiteStorage
        storage = SQLiteStorage(str(db_path))
        vault = TOTPVault(master_key=master_key, storage=storage)
        
        provider = MFAuthorizationProvider(vault)
        provider.set_confirmation_callback(lambda x: True)
        
        return provider
    
    def test_context_mapping(self, provider):
        """测试数据级别到上下文的映射"""
        assert provider.get_context_for_level(DataLevel.L3_RESTRICTED) == "l3_restricted_access"
        assert provider.get_context_for_level(DataLevel.L4_CONFIDENTIAL) == "l4_confidential_access"
        assert provider.get_context_for_level(DataLevel.L5_SECRET) == "l5_secret_access"
        assert provider.get_context_for_level(DataLevel.L6_CRITICAL) == "l6_critical_access"
        assert provider.get_context_for_level(DataLevel.L1_PUBLIC) is None
        assert provider.get_context_for_level(DataLevel.L2_INTERNAL) is None
    
    @pytest.mark.asyncio
    async def test_authorization_without_callback(self, provider):
        """测试未配置回调时的授权"""
        provider.set_confirmation_callback(None)
        
        from internal_control.reference_monitor import AccessRequest
        request = AccessRequest(
            agent_id="test-agent",
            file_path="~/test.txt",
            operation=AccessOperation.READ,
            context={},
            timestamp=datetime.now()
        )
        
        result = await provider.request_authorization(
            request=request,
            level=DataLevel.L3_RESTRICTED
        )
        
        assert result.decision == AccessDecision.DENY
        assert "not configured" in result.reason.lower()
    
    @pytest.mark.asyncio
    async def test_authorization_success(self, provider):
        """测试成功授权"""
        from internal_control.reference_monitor import AccessRequest
        
        request = AccessRequest(
            agent_id="test-agent",
            file_path="~/test.txt",
            operation=AccessOperation.READ,
            context={},
            timestamp=datetime.now()
        )
        
        result = await provider.request_authorization(
            request=request,
            level=DataLevel.L3_RESTRICTED
        )
        
        assert result.decision == AccessDecision.ALLOW
        assert result.token is not None
        assert result.level == DataLevel.L3_RESTRICTED
    
    @pytest.mark.asyncio
    async def test_low_level_no_mfa(self, provider):
        """测试低级别不需要 MFA"""
        from internal_control.reference_monitor import AccessRequest
        
        request = AccessRequest(
            agent_id="test-agent",
            file_path="~/test.txt",
            operation=AccessOperation.READ,
            context={},
            timestamp=datetime.now()
        )
        
        result = await provider.request_authorization(
            request=request,
            level=DataLevel.L1_PUBLIC
        )
        
        assert result.decision == AccessDecision.ALLOW
        assert "no_mfa_required" in result.policy.lower()


class TestReferenceMonitorWithMFA:
    """集成 Monitor 测试"""
    
    @pytest.fixture
    def temp_dir(self):
        temp = tempfile.mkdtemp()
        yield temp
        shutil.rmtree(temp)
    
    @pytest.mark.asyncio
    async def test_monitor_initialization(self, temp_dir):
        """测试 Monitor 初始化"""
        monitor = ReferenceMonitorWithMFA()
        await monitor.initialize()
        
        assert monitor.monitor is not None
        assert monitor.mfa_provider is not None
    
    def test_callback_setting(self):
        """测试回调设置"""
        monitor = ReferenceMonitorWithMFA()
        
        def test_callback(info):
            return True
        
        monitor.set_mfa_confirmation_callback(test_callback)
        assert monitor.mfa_provider._confirmation_callback == test_callback


def test_create_simple_console_callback():
    """测试控制台回调创建"""
    callback = create_simple_console_callback()
    assert callable(callback)


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"])
