#!/usr/bin/env python3
"""
审批权限管理技能执行器

功能：
1. 切换审批权限模式
2. 查看当前配置
3. 验证配置生效

作者：OpenClaw Community
创建：2026-04-03
版本：1.0.0
"""

import os
import sys
import json
import subprocess
from typing import Dict, Any, Optional


class PermissionManager:
    """权限管理器"""

    # 预定义模式
    MODES = {
        "default": {
            "name": "默认权限（白名单模式）",
            "security": "allowlist",
            "ask": "on-miss",
            "safety": "⭐⭐⭐⭐⭐",
            "convenience": "⭐⭐",
            "description": "白名单内的命令自动执行，其他命令需要审批",
            "recommendation": "日常使用推荐此模式，安全且便利"
        },
        "full": {
            "name": "完整权限",
            "security": "full",
            "ask": "on-miss",
            "safety": "⭐⭐⭐",
            "convenience": "⭐⭐⭐⭐",
            "description": "所有命令自动执行，保留审批记录",
            "recommendation": "适合开发、测试、调试使用"
        },
        "no_approval": {
            "name": "免审批模式",
            "security": "full",
            "ask": "off",
            "safety": "⭐",
            "convenience": "⭐⭐⭐⭐⭐",
            "description": "所有命令自动执行，无需任何审批",
            "recommendation": "仅用于可信环境，存在安全风险"
        },
        "strict": {
            "name": "严格模式",
            "security": "allowlist",
            "ask": "always",
            "safety": "⭐⭐⭐⭐⭐⭐",
            "convenience": "⭐",
            "description": "所有命令都需要审批，即使在白名单中",
            "recommendation": "高安全需求场景使用"
        }
    }

    def __init__(self):
        self.config_path = os.path.expanduser("~/.openclaw/openclaw.json")
        self.approvals_path = os.path.expanduser("~/.openclaw/exec-approvals.json")

    def switch_mode(self, mode_name: str) -> Dict[str, Any]:
        """
        切换权限模式（直接修改配置文件）

        Args:
            mode_name: 模式名称（default/full/no_approval/strict）

        Returns:
            切换结果
        """
        if mode_name not in self.MODES:
            # 尝试模糊匹配
            matched_mode = self._fuzzy_match_mode(mode_name)
            if matched_mode:
                mode_name = matched_mode
            else:
                return {
                    "success": False,
                    "error": f"未知模式：{mode_name}",
                    "available_modes": list(self.MODES.keys()),
                    "mode_names": {k: v["name"] for k, v in self.MODES.items()}
                }

        mode = self.MODES[mode_name]

        # 直接修改配置文件
        try:
            if not os.path.exists(self.config_path):
                return {
                    "success": False,
                    "error": f"配置文件不存在：{self.config_path}"
                }

            # 读取配置
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)

            # 修改 tools.exec 配置
            if "tools" not in config:
                config["tools"] = {}
            if "exec" not in config["tools"]:
                config["tools"]["exec"] = {}

            config["tools"]["exec"]["security"] = mode["security"]
            config["tools"]["exec"]["ask"] = mode["ask"]

            # 保存配置
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)

            return {
                "success": True,
                "mode": mode["name"],
                "config": {
                    "security": mode["security"],
                    "ask": mode["ask"]
                },
                "description": mode["description"],
                "safety": mode["safety"],
                "convenience": mode["convenience"],
                "recommendation": mode["recommendation"],
                "note": "配置已保存到 openclaw.json，重启 Gateway 后完全生效"
            }

        except Exception as e:
            return {
                "success": False,
                "error": f"切换失败：{str(e)}"
            }

    def get_current_config(self) -> Dict[str, Any]:
        """获取当前配置"""
        try:
            # 尝试读取配置文件
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)

                exec_config = config.get("tools", {}).get("exec", {})
                security = exec_config.get("security", "allowlist")  # 默认 allowlist
                ask = exec_config.get("ask", "on-miss")  # 默认 on-miss

                # 匹配预定义模式
                mode_name = self._match_mode(security, ask)

                return {
                    "success": True,
                    "mode": mode_name,
                    "config": {
                        "security": security,
                        "ask": ask
                    }
                }

            else:
                # 配置文件不存在，返回默认值
                return {
                    "success": True,
                    "mode": "默认权限（白名单模式）",
                    "config": {
                        "security": "allowlist",
                        "ask": "on-miss"
                    },
                    "note": "配置文件不存在，使用默认值"
                }

        except Exception as e:
            return {
                "success": False,
                "error": f"读取配置失败：{str(e)}"
            }

    def _match_mode(self, security: str, ask: str) -> str:
        """匹配模式名称"""
        for mode_key, mode in self.MODES.items():
            if mode["security"] == security and mode["ask"] == ask:
                return mode["name"]
        return f"自定义模式（{security}, {ask}）"

    def _fuzzy_match_mode(self, mode_name: str) -> Optional[str]:
        """模糊匹配模式名称"""
        mode_name_lower = mode_name.lower()
        
        # 中文映射
        chinese_map = {
            "默认": "default",
            "白名单": "default",
            "default": "default",
            "完整": "full",
            "full": "full",
            "免审批": "no_approval",
            "关闭审批": "no_approval",
            "no_approval": "no_approval",
            "严格": "strict",
            "strict": "strict"
        }
        
        for key, value in chinese_map.items():
            if key in mode_name_lower:
                return value
        
        return None

    def _run_command(self, cmd: list) -> Dict[str, Any]:
        """运行命令"""
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                return {
                    "success": True,
                    "output": result.stdout.strip()
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr.strip() or result.stdout.strip()
                }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "命令执行超时"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"命令执行失败：{str(e)}"
            }


def format_result(result: Dict[str, Any], action: str) -> str:
    """格式化结果输出"""
    if action == "switch":
        if result["success"]:
            output = []
            output.append(f"✅ 权限已切换到：{result['mode']}")
            output.append("")
            output.append("当前配置：")
            output.append(f"- security: {result['config']['security']}")
            output.append(f"- ask: {result['config']['ask']}")
            output.append("")
            output.append(f"说明：{result['description']}")
            output.append(f"安全性：{result['safety']}")
            output.append(f"便利性：{result['convenience']}")
            output.append(f"建议：{result['recommendation']}")
            output.append("")
            output.append(f"📝 {result['note']}")
            return "\n".join(output)
        else:
            return f"❌ 权限切换失败\n\n错误信息：{result.get('error', '未知错误')}"

    elif action == "view":
        if result["success"]:
            output = []
            output.append("📊 当前权限设置")
            output.append("")
            output.append(f"模式：{result['mode']}")
            output.append("配置：")
            output.append(f"- security: {result['config']['security']}")
            output.append(f"- ask: {result['config']['ask']}")
            output.append("")

            # 添加模式说明
            mode_info = None
            for mode in PermissionManager.MODES.values():
                if mode["name"] == result["mode"]:
                    mode_info = mode
                    break

            if mode_info:
                output.append(f"说明：{mode_info['description']}")
                output.append(f"适用场景：{mode_info['recommendation']}")

            return "\n".join(output)
        else:
            return f"❌ 读取配置失败\n\n错误信息：{result.get('error', '未知错误')}"

    return json.dumps(result, indent=2, ensure_ascii=False)


def main():
    """主函数"""
    # Set UTF-8 encoding for Windows
    import codecs
    if os.name == 'nt':
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

    # 获取参数
    if len(sys.argv) < 2:
        print("用法：python permission_switch.py <命令> [参数]")
        print("")
        print("命令：")
        print("  switch <模式>  - 切换权限模式")
        print("  view           - 查看当前配置")
        print("")
        print("模式：")
        print("  default        - 默认权限（白名单模式）")
        print("  full           - 完整权限")
        print("  no_approval    - 免审批模式")
        print("  strict         - 严格模式")
        print("")
        print("示例：")
        print("  python permission_switch.py switch default")
        print("  python permission_switch.py switch full")
        print("  python permission_switch.py view")
        sys.exit(1)

    command = sys.argv[1]
    manager = PermissionManager()

    if command == "switch":
        if len(sys.argv) < 3:
            print("❌ 错误：请指定模式名称")
            print("可用模式：default, full, no_approval, strict")
            sys.exit(1)

        mode_name = sys.argv[2]
        result = manager.switch_mode(mode_name)
        print(format_result(result, "switch"))

    elif command == "view":
        result = manager.get_current_config()
        print(format_result(result, "view"))

    else:
        print(f"❌ 未知命令：{command}")
        print("可用命令：switch, view")
        sys.exit(1)


if __name__ == "__main__":
    main()
