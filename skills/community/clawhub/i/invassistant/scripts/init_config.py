# -*- coding: utf-8 -*-
"""
InvAssistant — 配置初始化脚本
生成默认的 invassistant-config.json 配置文件。

用法:
  python init_config.py                       # 在 Skill 根目录生成配置
  python init_config.py /path/to/output       # 在指定目录生成配置
"""
import json
import sys
from pathlib import Path

DEFAULT_CONFIG = {
    "portfolio": {
        "_comment": "关注股票列表和策略配置。strategy 类型: redline(三条红线建仓) / hold(永久持有) / pullback(回调加仓) / satellite(卫星仓不动)。exit_params 配置退出条件（止盈/止损/趋势破位/动量衰竭）",
        "watchlist": [
            {
                "symbol": "TSLA",
                "name": "特斯拉",
                "strategy": "redline",
                "params": {
                    "emotion_drop_threshold": -4,
                    "consecutive_days": 3,
                    "ma_proximity": 0.03,
                    "bounce_threshold": 1.5,
                    "volume_ratio": 1.2,
                    "entry_size": 0.3
                },
                "exit_params": {
                    "_comment": "退出条件配置。cost_basis=0表示未持仓，填入实际成本价后启用止盈/止损检查",
                    "cost_basis": 0,
                    "position_size": 0,
                    "take_profit_enabled": True,
                    "take_profit_tiers": [
                        {"gain_pct": 20, "action": "减仓1/3", "reduce_pct": 33, "label": "第一阶梯止盈"},
                        {"gain_pct": 40, "action": "再减1/3", "reduce_pct": 33, "label": "第二阶梯止盈"},
                        {"gain_pct": 80, "action": "仅保留底仓", "reduce_pct": 50, "label": "大幅止盈"}
                    ],
                    "stop_loss_enabled": True,
                    "stop_loss_pct": -15,
                    "stop_loss_action": "清仓",
                    "trend_break_enabled": True,
                    "trend_break_ma": 50,
                    "trend_break_confirm_days": 3,
                    "trend_break_action": "减仓50%",
                    "trend_break_reduce_pct": 50,
                    "momentum_fade_enabled": True,
                    "momentum_action": "减仓1/3",
                    "momentum_reduce_pct": 33
                }
            },
            {
                "symbol": "NVDA",
                "name": "英伟达",
                "strategy": "hold",
                "exit_params": {
                    "_comment": "永久HOLD标的：仅在系统性风险时考虑退出，不配置常规止盈止损。cost_basis 填入后可追踪浮盈。趋势破位和动量衰竭仅做预警不做动作",
                    "cost_basis": 0,
                    "position_size": 0,
                    "take_profit_enabled": False,
                    "stop_loss_enabled": False,
                    "trend_break_enabled": True,
                    "trend_break_ma": 50,
                    "trend_break_confirm_days": 5,
                    "trend_break_action": "预警（HOLD标的不减仓，仅系统性风险时防守）",
                    "trend_break_reduce_pct": 0,
                    "momentum_fade_enabled": True,
                    "momentum_action": "预警（观察）",
                    "momentum_reduce_pct": 0
                }
            },
            {
                "symbol": "GOOGL",
                "name": "谷歌",
                "strategy": "pullback",
                "params": {
                    "pullback_threshold": 0.06,
                    "max_add_pct": 0.01
                },
                "exit_params": {
                    "cost_basis": 0,
                    "position_size": 0,
                    "take_profit_enabled": True,
                    "take_profit_tiers": [
                        {"gain_pct": 25, "action": "减仓1/4", "reduce_pct": 25, "label": "第一阶梯止盈"},
                        {"gain_pct": 50, "action": "减仓1/3", "reduce_pct": 33, "label": "第二阶梯止盈"}
                    ],
                    "stop_loss_enabled": True,
                    "stop_loss_pct": -12,
                    "stop_loss_action": "清仓",
                    "trend_break_enabled": True,
                    "trend_break_ma": 50,
                    "trend_break_confirm_days": 3,
                    "trend_break_action": "减仓50%",
                    "trend_break_reduce_pct": 50,
                    "momentum_fade_enabled": True,
                    "momentum_action": "减仓1/4",
                    "momentum_reduce_pct": 25
                }
            },
            {
                "symbol": "AMZN",
                "name": "亚马逊",
                "strategy": "pullback",
                "params": {
                    "pullback_threshold": 0.06,
                    "max_add_pct": 0.01
                },
                "exit_params": {
                    "cost_basis": 0,
                    "position_size": 0,
                    "take_profit_enabled": True,
                    "take_profit_tiers": [
                        {"gain_pct": 25, "action": "减仓1/4", "reduce_pct": 25, "label": "第一阶梯止盈"},
                        {"gain_pct": 50, "action": "减仓1/3", "reduce_pct": 33, "label": "第二阶梯止盈"}
                    ],
                    "stop_loss_enabled": True,
                    "stop_loss_pct": -12,
                    "stop_loss_action": "清仓",
                    "trend_break_enabled": True,
                    "trend_break_ma": 50,
                    "trend_break_confirm_days": 3,
                    "trend_break_action": "减仓50%",
                    "trend_break_reduce_pct": 50,
                    "momentum_fade_enabled": True,
                    "momentum_action": "减仓1/4",
                    "momentum_reduce_pct": 25
                }
            },
            {
                "symbol": "AAPL",
                "name": "苹果",
                "strategy": "hold",
                "exit_params": {
                    "cost_basis": 0,
                    "position_size": 0,
                    "take_profit_enabled": False,
                    "stop_loss_enabled": False,
                    "trend_break_enabled": True,
                    "trend_break_ma": 50,
                    "trend_break_confirm_days": 5,
                    "trend_break_action": "预警（HOLD标的不减仓）",
                    "trend_break_reduce_pct": 0,
                    "momentum_fade_enabled": True,
                    "momentum_action": "预警（观察）",
                    "momentum_reduce_pct": 0
                }
            },
            {
                "symbol": "META",
                "name": "Meta",
                "strategy": "hold",
                "exit_params": {
                    "cost_basis": 0,
                    "position_size": 0,
                    "take_profit_enabled": False,
                    "stop_loss_enabled": False,
                    "trend_break_enabled": True,
                    "trend_break_ma": 50,
                    "trend_break_confirm_days": 5,
                    "trend_break_action": "预警（HOLD标的不减仓）",
                    "trend_break_reduce_pct": 0,
                    "momentum_fade_enabled": True,
                    "momentum_action": "预警（观察）",
                    "momentum_reduce_pct": 0
                }
            },
            {
                "symbol": "PDD",
                "name": "拼多多",
                "strategy": "satellite",
                "exit_params": {
                    "_comment": "卫星仓：设置较紧的止损线，止盈则较宽",
                    "cost_basis": 0,
                    "position_size": 0,
                    "take_profit_enabled": True,
                    "take_profit_tiers": [
                        {"gain_pct": 30, "action": "减仓1/2", "reduce_pct": 50, "label": "卫星止盈"}
                    ],
                    "stop_loss_enabled": True,
                    "stop_loss_pct": -20,
                    "stop_loss_action": "清仓",
                    "trend_break_enabled": False,
                    "momentum_fade_enabled": False
                }
            },
            {
                "symbol": "LKNCY",
                "name": "瑞幸咖啡",
                "strategy": "satellite",
                "exit_params": {
                    "cost_basis": 0,
                    "position_size": 0,
                    "take_profit_enabled": True,
                    "take_profit_tiers": [
                        {"gain_pct": 30, "action": "减仓1/2", "reduce_pct": 50, "label": "卫星止盈"}
                    ],
                    "stop_loss_enabled": True,
                    "stop_loss_pct": -20,
                    "stop_loss_action": "清仓",
                    "trend_break_enabled": False,
                    "momentum_fade_enabled": False
                }
            }
        ],
        "market_indicators": ["QQQ", "^GSPC", "^VIX"],
        "vix_threshold": 25,
        "api_delay": 3,
        "api_retries": 3,
        "systemic_risk_exit": {
            "_comment": "系统性风险防守退出参数（全组合层级）。这是唯一可以覆盖HOLD策略的退出条件",
            "enabled": True,
            "vix_panic_threshold": 30,
            "vix_extreme_threshold": 40,
            "market_consecutive_drop_days": 3,
            "market_drop_magnitude": -2,
            "panic_action": "非核心仓减半",
            "extreme_action": "全组合减至50%"
        }
    },
    "adapters": {
        "wechatwork": {
            "enabled": False,
            "type": "webhook",
            "webhook_url": "",
            "_comment": "企业微信群机器人 Webhook URL (群设置 → 群机器人 → 添加自定义机器人 → 复制 Webhook 地址)"
        },
        "dingtalk": {
            "enabled": False,
            "type": "webhook",
            "webhook_url": "",
            "secret": "",
            "_comment": "钉钉群机器人 (群设置 → 智能群助手 → 添加机器人 → 自定义)。安全设置可选: 加签(填 secret)、关键词(设'信号''持仓')、IP白名单"
        },
        "feishu": {
            "enabled": False,
            "type": "webhook",
            "webhook_url": "",
            "secret": "",
            "_comment": "飞书群机器人 (群设置 → 群机器人 → 添加机器人 → 自定义机器人)。安全设置可选: 签名校验(填 secret)、关键词、IP白名单"
        }
    },
    "commands": {
        "_comment": "指令映射: 群机器人收到的指令 → 执行的动作。用于企微/钉钉/飞书群中 @机器人 发指令触发检查",
        "检查持仓": "full_check",
        "今日信号": "full_check",
        "TSLA红线": "tsla_detail",
        "详细分析": "tsla_detail",
        "帮助": "help"
    },
    "output": {
        "save_json": True,
        "json_dir": "output",
        "_comment": "检查结果输出目录，JSON 快照文件会保存在此目录下"
    }
}


def main():
    output_dir = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).parent.parent
    output_file = output_dir / "invassistant-config.json"

    if output_file.exists():
        print(f"[跳过] 配置文件已存在: {output_file}")
        print("  如需重新生成，请先删除现有文件")
        return

    output_dir.mkdir(parents=True, exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_CONFIG, f, ensure_ascii=False, indent=2)

    print(f"[成功] 配置文件已生成: {output_file}")
    print()
    print("📋 配置说明:")
    print("  1. 关注股票: portfolio.watchlist (添加/删除标的，修改策略类型)")
    print("  2. 推送渠道: adapters (填入 Webhook URL，设 enabled=true 启用)")
    print("  3. 指令映射: commands (自定义群机器人指令触发的动作)")
    print()
    print("📌 策略类型说明:")
    print("  - redline:   三条红线建仓 (情绪释放+技术止跌+市场环境)")
    print("  - hold:      永久持有，不加不减 (仅系统性风险时防守)")
    print("  - pullback:  回调加仓 (达到阈值时提示可小加)")
    print("  - satellite: 卫星仓，不动 (设较紧止损线)")
    print()
    print("📌 退出条件说明:")
    print("  - 止盈减仓: 浮盈达阶梯目标后分批锁利 (配置 exit_params.take_profit_tiers)")
    print("  - 止损清仓: 亏损超阈值立即清仓 (配置 exit_params.stop_loss_pct)")
    print("  - 趋势破位: 跌破关键均线且无承接 (配置 exit_params.trend_break_ma)")
    print("  - 动量衰竭: 创新高但缩量/MACD背离 (配置 exit_params.momentum_fade_enabled)")
    print("  - 系统风险: VIX恐慌+市场连续暴跌 (配置 portfolio.systemic_risk_exit)")
    print()
    print("⚠️ 重要: 填入 exit_params.cost_basis (持仓成本价) 后止盈/止损才会生效")


if __name__ == "__main__":
    main()
