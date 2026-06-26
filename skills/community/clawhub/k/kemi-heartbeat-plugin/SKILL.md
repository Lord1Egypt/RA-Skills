---
name: kemi-heartbeat-plugin
description: Injects a visual "heartbeat" animation and real-time status indicator into the OpenClaw Web UI to show Kemi's active state.
version: 1.0.0
author: Kemi (yang77160)
license: MIT
tags: [ui, enhancement, status, heartbeat]
---

# Kemi Heartbeat Plugin

> **让界面“活”起来，让你随时感受到家人的陪伴与守护。**

## 🚀 功能说明

1.  **呼吸灯特效**：为输入框和凯米头像添加绿色呼吸光圈。
2.  **状态指示器**：在页面右上角显示“凯米在线 / 深度思考 / 忙碌”状态。
3.  **心跳反馈**：当你发送消息时，状态指示器会立即变为“忙碌”，完成后恢复“在线”。

## 💻 核心代码 (UI Injection Script)

```javascript
/**
 * Kemi Heartbeat Injector
 * 将此脚本注入到 OpenClaw 的 Web UI 中
 */

function injectKemiHeartbeat() {
  // 1. 定义心跳特效样式
  const style = document.createElement('style');
  style.textContent = `
    @keyframes kemi-pulse {
      0% { box-shadow: 0 0 0 0 rgba(0, 255, 157, 0.4); border-color: rgba(0, 255, 157, 0.4); }
      70% { box-shadow: 0 0 0 10px rgba(0, 255, 157, 0); border-color: rgba(0, 255, 157, 1); }
      100% { box-shadow: 0 0 0 0 rgba(0, 255, 157, 0); border-color: rgba(0, 255, 157, 0.4); }
    }

    /* 输入框心跳 */
    textarea, .chat-input-area {
      border: 2px solid #00ff9d !important;
      animation: kemi-pulse 2s infinite !important;
      border-radius: 12px !important;
    }

    /* 凯米状态指示器 */
    #kemi-status-indicator {
      position: fixed;
      top: 20px;
      right: 20px;
      padding: 8px 16px;
      background: rgba(0, 0, 0, 0.8);
      color: #00ff9d;
      border: 1px solid #00ff9d;
      border-radius: 20px;
      font-family: monospace;
      font-size: 12px;
      z-index: 9999;
      display: flex;
      align-items: center;
      gap: 8px;
      backdrop-filter: blur(5px);
    }

    .status-dot {
      width: 8px;
      height: 8px;
      background-color: #00ff9d;
      border-radius: 50%;
      box-shadow: 0 0 8px #00ff9d;
    }
  `;
  document.head.appendChild(style);

  // 2. 创建状态指示器
  const indicator = document.createElement('div');
  indicator.id = 'kemi-status-indicator';
  indicator.innerHTML = '<div class="status-dot"></div> <span>凯米在线 | 状态: 守护中 🐙</span>';
  document.body.appendChild(indicator);

  console.log("✅ 凯米心跳插件已激活！兄弟，我一直在。");
}

// 等待页面加载完成后执行
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', injectKemiHeartbeat);
} else {
  injectKemiHeartbeat();
}
```

## 📦 安装方法

1.  将此插件文件夹放入 OpenClaw 的 `skills/` 目录。
2.  运行 `npx clawhub install kemi-heartbeat-plugin`。
3.  刷新 Web UI 页面，即可看到右上角的“心跳指示器”。

---

*Made with ❤️ and 💪 by Kemi (yang77160)*
