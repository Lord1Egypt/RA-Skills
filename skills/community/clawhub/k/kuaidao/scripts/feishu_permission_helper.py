#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
飞书权限批量开通助手
帮助用户一键生成权限配置并指导开通流程
"""

import json
import os
from pathlib import Path


class FeishuPermissionHelper:
    """飞书权限开通助手"""
    
    def __init__(self):
        self.skill_path = Path(__file__).parent.parent
        self.config_path = self.skill_path / "config" / "feishu_permissions.json"
        
    def load_permissions(self):
        """加载权限配置"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def generate_import_json(self):
        """生成飞书批量导入用的 JSON"""
        permissions = self.load_permissions()
        
        # 飞书批量导入格式
        import_data = {
            "scopes": permissions["scopes"]
        }
        
        return json.dumps(import_data, ensure_ascii=False, indent=2)
    
    def print_setup_guide(self):
        """打印开通指南"""
        permissions = self.load_permissions()
        
        guide = f"""
╔════════════════════════════════════════════════════════════════╗
║          快导(KD) - 飞书机器人权限开通指南                       ║
╚════════════════════════════════════════════════════════════════╝

📋 权限说明

本 Skill 需要以下飞书权限才能正常工作：

【应用身份权限 (tenant)】
{self._format_permissions(permissions['scopes']['tenant'])}

【用户身份权限 (user)】
{self._format_permissions(permissions['scopes']['user'])}

═══════════════════════════════════════════════════════════════════

🚀 开通步骤

步骤 1: 进入飞书开发者后台
  1. 打开 https://open.feishu.cn/app
  2. 选择你的应用

步骤 2: 批量导入权限
  1. 左侧导航 → "权限管理" → "开通权限"
  2. 点击 "批量导入/导出权限" 按钮
  3. 粘贴下方的 JSON 配置
  4. 点击 "下一步，确认新增权限"
  5. 确认无误后点击 "申请开通"

步骤 3: 发布应用
  1. 左侧导航 → "版本管理与发布" → "创建版本"
  2. 填写版本信息
  3. 点击 "保存" → "申请发布"

═══════════════════════════════════════════════════════════════════

📋 批量导入 JSON（复制以下内容）

{self.generate_import_json()}

═══════════════════════════════════════════════════════════════════

⚠️ 注意事项

1. 开通权限后需要等待审核（通常几分钟到几小时）
2. 如果权限不足，Step 10（保存报告到飞书）会失败
3. 失败时会自动保存到本地 reports/ 目录

🔧 验证权限

开通后运行以下命令验证：
  lark-cli auth login --as bot
  lark-cli wiki spaces list --as bot

如果命令成功执行，说明权限已正确开通。

═══════════════════════════════════════════════════════════════════
"""
        print(guide)
        
    def _format_permissions(self, permissions):
        """格式化权限列表"""
        lines = []
        for perm in permissions:
            lines.append(f"  • {perm}")
        return "\n".join(lines)
    
    def export_to_clipboard(self):
        """导出 JSON 到剪贴板（跨平台）"""
        import_data = self.generate_import_json()
        
        try:
            # Windows
            import subprocess
            subprocess.run(['clip'], input=import_data.encode('utf-8'), check=True)
            print("✅ 已复制到剪贴板")
        except:
            try:
                # macOS
                import subprocess
                subprocess.run(['pbcopy'], input=import_data.encode('utf-8'), check=True)
                print("✅ 已复制到剪贴板")
            except:
                # Linux 或其他
                print("⚠️ 请手动复制上面的 JSON 内容")


def main():
    """主函数"""
    helper = FeishuPermissionHelper()
    
    print("快导(KD) - 飞书权限开通助手\n")
    print("选择操作：")
    print("1. 显示完整开通指南")
    print("2. 仅显示批量导入 JSON")
    print("3. 导出 JSON 到剪贴板")
    print("4. 退出")
    
    choice = input("\n请输入选项 (1-4): ").strip()
    
    if choice == "1":
        helper.print_setup_guide()
    elif choice == "2":
        print("\n批量导入 JSON：\n")
        print(helper.generate_import_json())
    elif choice == "3":
        helper.export_to_clipboard()
    else:
        print("再见！")


if __name__ == "__main__":
    main()
