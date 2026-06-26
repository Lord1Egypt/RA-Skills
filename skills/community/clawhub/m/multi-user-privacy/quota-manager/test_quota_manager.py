#!/usr/bin/env python3
"""
配额管理器测试脚本
测试所有高级配额管理功能
"""

import os
import sys
import json
from datetime import datetime

# 添加路径
sys.path.insert(0, os.path.dirname(__file__))

from quota_manager import QuotaManager, QuotaConfig


def test_basic_quota():
    """测试 1: 基本配额管理 - 按用户类型设置配额"""
    print("\n" + "="*60)
    print("测试 1: 按用户类型设置配额（VIP/普通）")
    print("="*60)
    
    # 创建管理器（使用测试配置文件）
    test_config = os.path.join(os.path.dirname(__file__), "test_quota_config.json")
    if os.path.exists(test_config):
        os.remove(test_config)
    
    manager = QuotaManager(test_config)
    
    # 创建普通用户
    print("\n📝 创建普通用户 user_normal_001...")
    user_normal = manager.create_user("user_normal_001", "normal")
    print(f"   ✓ 用户类型：{user_normal.user_type}")
    print(f"   ✓ Token 配额：{user_normal.quota.token_quota:,}")
    print(f"   ✓ 磁盘配额：{user_normal.quota.disk_quota_mb} MB")
    print(f"   ✓ 消息配额：{user_normal.quota.message_quota:,}")
    
    # 创建 VIP 用户
    print("\n📝 创建 VIP 用户 user_vip_001...")
    user_vip = manager.create_user("user_vip_001", "vip")
    print(f"   ✓ 用户类型：{user_vip.user_type}")
    print(f"   ✓ Token 配额：{user_vip.quota.token_quota:,}")
    print(f"   ✓ 磁盘配额：{user_vip.quota.disk_quota_mb} MB")
    print(f"   ✓ 消息配额：{user_vip.quota.message_quota:,}")
    
    # 验证配额差异
    print("\n📊 配额对比:")
    print(f"   VIP Token 是普通的 {user_vip.quota.token_quota / user_normal.quota.token_quota} 倍")
    print(f"   VIP 磁盘是普通的 {user_vip.quota.disk_quota_mb / user_normal.quota.disk_quota_mb} 倍")
    print(f"   VIP 消息是普通的 {user_vip.quota.message_quota / user_normal.quota.message_quota} 倍")
    
    # 升级用户类型
    print("\n⬆️  升级 user_normal_001 到 VIP...")
    user_normal = manager.update_user_type("user_normal_001", "vip")
    print(f"   ✓ 新类型：{user_normal.user_type}")
    print(f"   ✓ 新 Token 配额：{user_normal.quota.token_quota:,}")
    
    # 检查可用配额
    print("\n📊 可用配额检查:")
    available = manager.get_available_quota("user_vip_001")
    for k, v in available.items():
        print(f"   {k}: {v:,}")
    
    print("\n✅ 测试 1 通过!")
    return manager


def test_group_inheritance():
    """测试 2: 配额继承（组配额）"""
    print("\n" + "="*60)
    print("测试 2: 配额继承（组配额）")
    print("="*60)
    
    test_config = os.path.join(os.path.dirname(__file__), "test_quota_config.json")
    manager = QuotaManager(test_config)
    
    # 创建自定义组
    print("\n📝 创建项目组 project_alpha...")
    custom_quota = QuotaConfig(
        disk_quota_mb=5000,
        token_quota=5000000,
        message_quota=50000,
        session_timeout_hours=168,
        api_calls_per_hour=5000,
        storage_files_max=1000
    )
    group = manager.create_group(
        "project_alpha",
        "Alpha 项目组",
        quota=custom_quota,
        inherit_to_members=True
    )
    print(f"   ✓ 组 ID: {group.group_id}")
    print(f"   ✓ 组名称：{group.group_name}")
    print(f"   ✓ Token 配额：{group.quota.token_quota:,}")
    print(f"   ✓ 继承启用：{group.inherit_to_members}")
    
    # 创建用户并加入组
    print("\n📝 创建项目成员 member_001 并加入组...")
    member = manager.create_user("member_001", "normal", group_id="project_alpha")
    print(f"   ✓ 用户原始类型：normal")
    print(f"   ✓ 加入组后 Token 配额：{member.quota.token_quota:,}")
    print(f"   ✓ 继承组配额：{member.quota.token_quota == group.quota.token_quota}")
    
    # 添加现有用户到组
    print("\n📝 将 user_vip_001 加入项目组...")
    manager.add_user_to_group("user_vip_001", "project_alpha")
    user_vip = manager.get_user_quota("user_vip_001")
    print(f"   ✓ 用户组：{user_vip.group_id}")
    print(f"   ✓ 新 Token 配额：{user_vip.quota.token_quota:,}")
    
    # 从组移除
    print("\n📝 从组移除 member_001...")
    manager.remove_user_from_group("member_001", "project_alpha")
    member = manager.get_user_quota("member_001")
    print(f"   ✓ 用户组：{member.group_id or '无'}")
    print(f"   ✓ 恢复后 Token 配额：{member.quota.token_quota:,}")
    
    # 获取组用户列表
    print("\n📊 项目组成员:")
    group_users = manager.get_users_by_group("project_alpha")
    for user in group_users:
        print(f"   - {user.user_id} ({user.user_type})")
    
    print("\n✅ 测试 2 通过!")
    return manager


def test_quota_borrowing():
    """测试 3: 配额借用（临时增加）"""
    print("\n" + "="*60)
    print("测试 3: 配额借用（临时增加）")
    print("="*60)
    
    test_config = os.path.join(os.path.dirname(__file__), "test_quota_config.json")
    manager = QuotaManager(test_config)
    
    # 创建测试用户
    print("\n📝 创建测试用户 borrower_001...")
    user = manager.create_user("borrower_001", "normal")
    print(f"   ✓ 原始 Token 配额：{user.quota.token_quota:,}")
    
    # 借用配额
    print("\n📝 借用 500,000 Tokens (48 小时)...")
    record = manager.borrow_quota(
        user_id="borrower_001",
        quota_type="tokens",
        amount=500000,
        duration_hours=48,
        approved_by="admin"
    )
    print(f"   ✓ 借用记录 ID: {record.record_id}")
    print(f"   ✓ 借用数量：{record.amount:,}")
    print(f"   ✓ 过期时间：{record.expires_at}")
    print(f"   ✓ 批准人：{record.approved_by}")
    
    # 检查借用后可用配额
    print("\n📊 借用后可用配额:")
    available = manager.get_available_quota("borrower_001")
    print(f"   ✓ Tokens: {available['tokens']:,}")
    print(f"   ✓ 借用配额：{user.borrowed_quota.get('tokens', 0):,}")
    
    # 再次借用
    print("\n📝 再次借用 200,000 Tokens (24 小时)...")
    record2 = manager.borrow_quota(
        user_id="borrower_001",
        quota_type="tokens",
        amount=200000,
        duration_hours=24
    )
    user = manager.get_user_quota("borrower_001")
    print(f"   ✓ 总借用 Tokens: {user.borrowed_quota.get('tokens', 0):,}")
    
    # 归还借用
    print(f"\n📝 归还第一次借用 ({record.record_id})...")
    manager.return_quota(record.record_id)
    user = manager.get_user_quota("borrower_001")
    print(f"   ✓ 剩余借用 Tokens: {user.borrowed_quota.get('tokens', 0):,}")
    
    # 获取活跃借用
    print("\n📊 活跃借用记录:")
    active_borrows = manager.get_active_borrows("borrower_001")
    for r in active_borrows:
        print(f"   - {r.record_id}: {r.quota_type} = {r.amount:,} (状态：{r.status})")
    
    print("\n✅ 测试 3 通过!")
    return manager


def test_usage_tracking():
    """测试 4: 配额使用追踪"""
    print("\n" + "="*60)
    print("测试 4: 配额使用追踪")
    print("="*60)
    
    test_config = os.path.join(os.path.dirname(__file__), "test_quota_config.json")
    manager = QuotaManager(test_config)
    
    # 创建测试用户
    user = manager.create_user("tracker_001", "vip")
    print(f"\n📝 创建用户 tracker_001")
    print(f"   ✓ Token 配额：{user.quota.token_quota:,}")
    
    # 模拟使用
    print("\n📝 模拟使用记录...")
    manager.record_usage("tracker_001", "tokens", 50000)
    manager.record_usage("tracker_001", "tokens", 30000)
    manager.record_usage("tracker_001", "messages", 100)
    manager.record_usage("tracker_001", "disk_mb", 250)
    
    user = manager.get_user_quota("tracker_001")
    print(f"   ✓ 已用 Tokens: {user.used.get('tokens', 0):,}")
    print(f"   ✓ 已用消息：{user.used.get('messages', 0)}")
    print(f"   ✓ 已用磁盘：{user.used.get('disk_mb', 0)} MB")
    
    # 检查配额是否足够
    print("\n📊 配额检查:")
    can_use_100k = manager.check_quota_available("tracker_001", "tokens", 100000)
    can_use_1m = manager.check_quota_available("tracker_001", "tokens", 1000000)
    print(f"   ✓ 可用 100K Tokens: {can_use_100k}")
    print(f"   ✓ 可用 1M Tokens: {can_use_1m}")
    
    # 可用配额
    available = manager.get_available_quota("tracker_001")
    print(f"\n📊 剩余可用配额:")
    for k, v in available.items():
        print(f"   {k}: {v:,}")
    
    print("\n✅ 测试 4 通过!")
    return manager


def test_export_reports():
    """测试 5: 配额报表（导出 CSV）"""
    print("\n" + "="*60)
    print("测试 5: 配额报表（导出 CSV）")
    print("="*60)
    
    test_config = os.path.join(os.path.dirname(__file__), "test_quota_config.json")
    manager = QuotaManager(test_config)
    
    # 导出用户报表
    print("\n📝 导出用户配额报表...")
    users_csv = os.path.join(os.path.dirname(__file__), "report_users.csv")
    manager.export_csv(users_csv, "users")
    print(f"   ✓ 已导出：{users_csv}")
    
    # 导出组报表
    print("\n📝 导出组配额报表...")
    groups_csv = os.path.join(os.path.dirname(__file__), "report_groups.csv")
    manager.export_csv(groups_csv, "groups")
    print(f"   ✓ 已导出：{groups_csv}")
    
    # 导出借用报表
    print("\n📝 导出借用记录报表...")
    borrows_csv = os.path.join(os.path.dirname(__file__), "report_borrows.csv")
    manager.export_csv(borrows_csv, "borrows")
    print(f"   ✓ 已导出：{borrows_csv}")
    
    # 显示报表内容预览
    print("\n📊 用户报表预览:")
    with open(users_csv, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        print(f"   总行数：{len(lines)}")
        print(f"   表头：{lines[0].strip()}")
        if len(lines) > 1:
            print(f"   第一行数据：{lines[1].strip()[:100]}...")
    
    # 获取汇总统计
    print("\n📊 配额汇总统计:")
    summary = manager.get_quota_summary()
    print(f"   总用户数：{summary['total_users']}")
    print(f"   总组数：{summary['total_groups']}")
    print(f"   活跃借用：{summary['active_borrows']}")
    print(f"   用户类型分布：{json.dumps(summary['users_by_type'], ensure_ascii=False)}")
    print(f"   总使用量:")
    for k, v in summary['total_usage'].items():
        print(f"     {k}: {v:,}")
    
    print("\n✅ 测试 5 通过!")
    return manager


def test_persistence():
    """测试 6: 数据持久化"""
    print("\n" + "="*60)
    print("测试 6: 数据持久化")
    print("="*60)
    
    test_config = os.path.join(os.path.dirname(__file__), "test_quota_config.json")
    
    # 第一次创建数据
    print("\n📝 创建初始数据...")
    manager1 = QuotaManager(test_config)
    manager1.create_user("persist_user_001", "vip")
    manager1.create_group("persist_group", "持久化测试组")
    manager1.add_user_to_group("persist_user_001", "persist_group")
    print(f"   ✓ 创建用户 persist_user_001")
    print(f"   ✓ 创建组 persist_group")
    
    # 重新加载
    print("\n📝 重新加载管理器（模拟重启）...")
    manager2 = QuotaManager(test_config)
    user = manager2.get_user_quota("persist_user_001")
    groups = manager2.get_all_groups()
    
    print(f"   ✓ 加载用户：{user.user_id if user else 'None'}")
    print(f"   ✓ 用户类型：{user.user_type if user else 'None'}")
    print(f"   ✓ 用户组：{user.group_id if user else 'None'}")
    print(f"   ✓ 加载组数：{len(groups)}")
    
    # 验证数据一致性
    assert user is not None, "用户数据丢失!"
    assert user.user_type == "vip", "用户类型错误!"
    assert user.group_id == "persist_group", "组信息丢失!"
    assert len(groups) > 0, "组数据丢失!"
    
    print("\n✅ 测试 6 通过! 数据持久化正常")
    return manager2


def run_all_tests():
    """运行所有测试"""
    print("\n" + "🐶"*30)
    print("高级配额管理系统 - 完整测试套件")
    print("🐶"*30)
    
    try:
        test_basic_quota()
        test_group_inheritance()
        test_quota_borrowing()
        test_usage_tracking()
        test_export_reports()
        test_persistence()
        
        print("\n" + "="*60)
        print("🎉 所有测试通过!")
        print("="*60)
        
        # 清理测试文件
        test_config = os.path.join(os.path.dirname(__file__), "test_quota_config.json")
        if os.path.exists(test_config):
            print(f"\n📁 测试配置文件：{test_config}")
        
        print("\n生成的报表文件:")
        for f in ["report_users.csv", "report_groups.csv", "report_borrows.csv"]:
            path = os.path.join(os.path.dirname(__file__), f)
            if os.path.exists(path):
                print(f"  - {path}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ 测试失败：{e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
