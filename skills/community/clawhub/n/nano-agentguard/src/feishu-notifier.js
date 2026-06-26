/**
 * Feishu Notifier for AgentGuard
 *
 * Send approval requests to Feishu
 */

const https = require('https');
const http = require('http');

class FeishuNotifier {
  constructor(options = {}) {
    this.webhookUrl = options.webhookUrl || process.env.FEISHU_WEBHOOK_URL;
    this.openId = options.openId || process.env.FEISHU_OPEN_ID;
    this.channel = options.channel || 'feishu';

    // If using OpenClaw message tool
    this.useOpenClaw = options.useOpenClaw !== false;
  }

  /**
   * Send approval request via Feishu
   */
  async sendApprovalRequest(request) {
    const message = this.formatApprovalCard(request);

    if (this.useOpenClaw) {
      // Return message payload for OpenClaw to send
      return {
        channel: this.channel,
        target: this.openId ? `user:${this.openId}` : null,
        message: message.text,
        card: message.card
      };
    }

    // Direct webhook (if configured)
    if (this.webhookUrl) {
      return this.sendWebhook(message.card || message.text);
    }

    throw new Error('No Feishu delivery method configured');
  }

  /**
   * Format approval request as Feishu interactive card
   */
  formatApprovalCard(request) {
    const text = `🔐 **审批请求**

**智能体**: ${request.agentId}
**操作**: ${request.operation}
**时间**: ${new Date(request.createdAt).toLocaleString('zh-CN')}
**过期**: ${new Date(request.expiresAt).toLocaleString('zh-CN')}

**详情**:
\`\`\`
${JSON.stringify(request.details, null, 2)}
\`\`\`

---
**请求ID**: \`${request.id}\`

批准命令: \`agentguard approve ${request.id}\`
拒绝命令: \`agentguard deny ${request.id}\``;

    // Feishu interactive card
    const card = {
      "config": {
        "wide_screen_mode": true
      },
      "header": {
        "title": {
          "tag": "plain_text",
          "content": "🔐 AgentGuard 审批请求"
        },
        "template": "orange"
      },
      "elements": [
        {
          "tag": "div",
          "fields": [
            {
              "is_short": true,
              "text": {
                "tag": "lark_md",
                "content": `**智能体**\n${request.agentId}`
              }
            },
            {
              "is_short": true,
              "text": {
                "tag": "lark_md",
                "content": `**操作**\n${request.operation}`
              }
            }
          ]
        },
        {
          "tag": "div",
          "fields": [
            {
              "is_short": true,
              "text": {
                "tag": "lark_md",
                "content": `**创建时间**\n${new Date(request.createdAt).toLocaleString('zh-CN')}`
              }
            },
            {
              "is_short": true,
              "text": {
                "tag": "lark_md",
                "content": `**过期时间**\n${new Date(request.expiresAt).toLocaleString('zh-CN')}`
              }
            }
          ]
        },
        {
          "tag": "hr"
        },
        {
          "tag": "div",
          "text": {
            "tag": "lark_md",
            "content": `**详情**\n\`\`\`json\n${JSON.stringify(request.details, null, 2)}\n\`\`\``
          }
        },
        {
          "tag": "note",
          "elements": [
            {
              "tag": "plain_text",
              "content": `请求ID: ${request.id}`
            }
          ]
        },
        {
          "tag": "action",
          "actions": [
            {
              "tag": "button",
              "text": {
                "tag": "plain_text",
                "content": "✅ 批准"
              },
              "type": "primary",
              "value": {
                "action": "approve",
                "requestId": request.id
              }
            },
            {
              "tag": "button",
              "text": {
                "tag": "plain_text",
                "content": "❌ 拒绝"
              },
              "type": "danger",
              "value": {
                "action": "deny",
                "requestId": request.id
              }
            }
          ]
        }
      ]
    };

    return { text, card };
  }

  /**
   * Send via webhook
   */
  async sendWebhook(payload) {
    return new Promise((resolve, reject) => {
      const url = new URL(this.webhookUrl);
      const client = url.protocol === 'https:' ? https : http;

      const data = JSON.stringify({
        msg_type: 'interactive',
        card: payload
      });

      const options = {
        hostname: url.hostname,
        port: url.port || (url.protocol === 'https:' ? 443 : 80),
        path: url.pathname,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': data.length
        }
      };

      const req = client.request(options, (res) => {
        let body = '';
        res.on('data', chunk => body += chunk);
        res.on('end', () => {
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve({ success: true, body });
          } else {
            reject(new Error(`Webhook failed: ${res.statusCode} ${body}`));
          }
        });
      });

      req.on('error', reject);
      req.write(data);
      req.end();
    });
  }

  /**
   * Send approval result notification
   */
  async sendApprovalResult(request, approved, by) {
    const status = approved ? '✅ 已批准' : '❌ 已拒绝';
    const color = approved ? 'green' : 'red';

    const card = {
      "config": {
        "wide_screen_mode": true
      },
      "header": {
        "title": {
          "tag": "plain_text",
          "content": `${status} - AgentGuard`
        },
        "template": color
      },
      "elements": [
        {
          "tag": "div",
          "fields": [
            {
              "is_short": true,
              "text": {
                "tag": "lark_md",
                "content": `**智能体**\n${request.agentId}`
              }
            },
            {
              "is_short": true,
              "text": {
                "tag": "lark_md",
                "content": `**操作**\n${request.operation}`
              }
            }
          ]
        },
        {
          "tag": "div",
          "text": {
            "tag": "lark_md",
            "content": `**处理人**: ${by}\n**时间**: ${new Date().toLocaleString('zh-CN')}`
          }
        }
      ]
    };

    return {
      channel: this.channel,
      target: this.openId ? `user:${this.openId}` : null,
      card
    };
  }
}

module.exports = FeishuNotifier;
