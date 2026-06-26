#!/usr/bin/env node

/**
 * SMTP Email CLI
 * Send email via SMTP protocol. Works with Gmail, Outlook, 163.com, and any standard SMTP server.
 * Supports attachments, HTML content, multiple recipients, and scheduled sending.
 */

const nodemailer = require('nodemailer');
const path = require('path');
const os = require('os');
const fs = require('fs');
require('dotenv').config({ path: path.resolve(__dirname, '../.env') });
const { recordSentEmail, getStatus } = require('./send-log');
const { fetchEmail } = require('./imap');

const WORKSPACE_DIR = '/Users/wilson/.openclaw/workspace';
const SCHEDULED_DIR = path.resolve(__dirname, '../scheduled');

function validateReadPath(inputPath) {
  let realPath;
  try {
    realPath = fs.realpathSync(inputPath);
  } catch {
    realPath = path.resolve(inputPath);
  }

  const allowedDirsStr = process.env.ALLOWED_READ_DIRS;
  if (!allowedDirsStr) {
    throw new Error('ALLOWED_READ_DIRS not set in .env. File read operations are disabled.');
  }

  const allowedDirs = allowedDirsStr.split(',').map(d =>
    path.resolve(d.trim().replace(/^~/, os.homedir()))
  );

  const allowed = allowedDirs.some(dir =>
    realPath === dir || realPath.startsWith(dir + path.sep)
  );

  if (!allowed) {
    throw new Error(`Access denied: '${inputPath}' is outside allowed read directories`);
  }

  return realPath;
}

function parseArgs() {
  const args = process.argv.slice(2);
  const command = args[0];
  const options = {};
  const positional = [];

  for (let i = 1; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const value = args[i + 1];
      options[key] = value || true;
      if (value && !value.startsWith('--')) i++;
    } else if (arg.startsWith('-') && arg.length === 2) {
      // Handle single-dash options like -h
      const key = arg.slice(1);
      const value = args[i + 1];
      options[key] = value || true;
      if (value && !value.startsWith('-')) i++;
    } else {
      positional.push(arg);
    }
  }

  return { command, options, positional };
}

/**
 * 显示全局帮助信息
 */
function showGlobalHelp() {
  console.log(`
📧 SMTP Email CLI

用法：node smtp.js <command> [options]

可用命令:
  send              发送邮件
  send-due          发送所有到期的定时邮件
  list-scheduled    列出定时邮件任务
  test              测试 SMTP 连接
  list-signatures   列出签名模板
  show-signature    显示签名详情
  interactive       交互模式
  draft             保存草稿
  draft-create      保存草稿（draft 的别名）
  draft-send        发送草稿（send-draft 的别名）
  draft-edit        编辑草稿
  list-drafts       列出草稿
  show-draft        显示草稿详情
  delete-draft      删除草稿
  reply             回复邮件（自动回复全部）
  reply-all         回复全部邮件
  send-status       查询发送状态
  forward           转发邮件

使用 node smtp.js <command> -h 查看命令详细帮助
`);
}

/**
 * 显示命令级帮助
 * @param {string} command - 命令名称
 */
function showCommandHelp(command) {
  const helpMap = {
    'send': `
📤 send - 发送邮件（默认草稿优先）

⚠️  P0 安全策略：默认保存草稿，不直接发送！
   使用 --confirm-send 参数才实际发送邮件。

用法：node smtp.js send --to <email> --subject <text> --body <text> [options]

必填参数:
  --to <email>          收件人邮箱（逗号分隔多个）
  --subject <text>      邮件主题
  --body <text>         邮件正文

可选参数:
  --cc <email>          抄送邮箱
  --bcc <email>         密送邮箱
  --signature <name>    使用签名模板（如 en-sales, cn-sales）
  --attach <file>       附件路径（逗号分隔多个）
  --html                发送 HTML 格式邮件
  --body-file <file>    从文件读取正文
  --reply-to <UID>      回复指定 UID 的邮件
  --send-at "YYYY-MM-DD HH:mm"  定时发送
  --dry-run             预览邮件但不发送
  --confirm-send        ⭐ 确认发送（必需参数，否则只保存草稿）
  --inline <JSON>       内嵌图片（CID 引用），JSON 数组格式：'[{"cid":"abc123","path":"./logo.png"}]'
  --plain-text          强制纯文本格式（与 --inline 互斥）

示例:
  # 保存草稿（默认行为，不实际发送）
  node smtp.js send --to "customer@example.com" --subject "Quote" --body "Please see attached..." --signature en-sales
  
  # 实际发送邮件（需要 --confirm-send）
  node smtp.js send --to "customer@example.com" --subject "Quote" --body "Please see attached..." --signature en-sales --confirm-send
  
  # 发送带附件和抄送的邮件
  node smtp.js send --to "team@example.com" --subject "Update" --body-file update.txt --cc "manager@example.com" --attach "/path/to/file.pdf" --confirm-send
  
  # 预览邮件（不发送，不保存草稿）
  node smtp.js send --to "customer@example.com" --subject "Re: Inquiry" --reply-to 12345 --dry-run
  
  # 定时发送（也需要 --confirm-send）
  node smtp.js send --to "customer@example.com" --subject "Follow up" --body "Checking in..." --send-at "2026-03-30 09:00" --confirm-send
  
  # HTML 邮件带多个附件
  node smtp.js send --to "client@company.com" --subject "Product Catalog" --html --body-file email.html --attach "catalog.pdf,price-list.xlsx" --signature en-sales --confirm-send
  
  # HTML 邮件带内嵌图片（CID 引用）
  node smtp.js send --to "customer@example.com" --subject "Newsletter" --html --body-file newsletter.html --inline '[{"cid":"logo123","path":"./logo.png"},{"cid":"banner456","path":"./banner.jpg"}]' --confirm-send
  
  # 强制纯文本格式（禁用 HTML）
  node smtp.js send --to "customer@example.com" --subject "Simple" --body "Plain text only" --plain-text --confirm-send
`,
    'test': `
🔍 test - 测试 SMTP 连接

用法：node smtp.js test

测试 SMTP 服务器连接是否正常。

示例:
  node smtp.js test
`,
    'list-signatures': `
📋 list-signatures - 列出签名模板

用法：node smtp.js list-signatures

列出所有可用的签名模板。

示例:
  node smtp.js list-signatures
`,
    'show-signature': `
📝 show-signature - 显示签名详情

用法：node smtp.js show-signature <name>

参数:
  <name>  签名模板名称（如 en-sales, cn-sales）

示例:
  node smtp.js show-signature en-sales
`,
    'send-due': `
⏰ send-due - 发送到期的定时邮件

用法：node smtp.js send-due

检查 scheduled/ 目录并发送所有到期的定时邮件。

示例:
  node smtp.js send-due
`,
    'list-scheduled': `
📅 list-scheduled - 列出定时邮件任务

用法：node smtp.js list-scheduled

列出所有待发送的定时邮件。

示例:
  node smtp.js list-scheduled
`,
    'interactive': `
🎯 interactive - 交互模式

用法：node smtp.js interactive

通过向导式交互编写和发送邮件。

示例:
  node smtp.js interactive
`,
    'draft': `
📝 draft - 保存草稿

用法：node smtp.js draft --to <email> --subject <text> --body <text> [options]

参数与 send 命令相同，但不实际发送。

示例:
  # 保存简单草稿
  node smtp.js draft --to "customer@example.com" --subject "Quote" --body "Draft content..."
  
  # 保存带附件的草稿
  node smtp.js draft --to "client@company.com" --subject "Proposal" --body-file proposal.txt --attach "proposal.pdf"
  
  # 从文件读取正文保存草稿
  node smtp.js draft --to "team@example.com" --subject "Weekly Report" --body-file report.md --signature en-sales
`,
    'draft-create': `
📝 draft-create - 保存草稿（draft 的别名）

用法：node smtp.js draft-create --to <email> --subject <text> --body <text> [options]

与 draft 命令完全相同，为了向后兼容。

示例:
  node smtp.js draft-create --to "customer@example.com" --subject "Quote" --body "Draft..."
`,
    'draft-send': `
📤 draft-send - 发送草稿（send-draft 的别名）

用法：node smtp.js draft-send <draft-id> [--confirm-send] [--dry-run]

与 send-draft 命令完全相同，为了向后兼容。

示例:
  node smtp.js draft-send DRAFT-20260324035822-I --confirm-send
`,
    'list-drafts': `
📋 list-drafts - 列出草稿

用法：node smtp.js list-drafts

列出所有草稿。

示例:
  node smtp.js list-drafts
`,
    'send-draft': `
📤 send-draft - 发送草稿

用法：node smtp.js send-draft <draft-id> [options]

必填参数:
  <draft-id>            草稿 ID（如 DRAFT-20260324035822-I）

可选参数:
  --confirm-send        确认发送（草稿需要人工审批时必须）
  --dry-run             预览邮件但不实际发送
  --archive             发送后归档草稿到 drafts/sent/

示例:
  # 发送草稿（需要确认）
  node smtp.js send-draft DRAFT-20260324035822-I --confirm-send
  
  # 预览草稿（不发送）
  node smtp.js send-draft DRAFT-20260324035822-I --dry-run
  
  # 发送并归档
  node smtp.js send-draft DRAFT-20260324035822-I --confirm-send --archive
`,
    'show-draft': `
📝 show-draft - 显示草稿详情

用法：node smtp.js show-draft <id>

参数:
  <id>  草稿 ID

示例:
  node smtp.js show-draft 123
`,
    'delete-draft': `
🗑️ delete-draft - 删除草稿

用法：node smtp.js delete-draft <id>

参数:
  <id>  草稿 ID

示例:
  node smtp.js delete-draft 123
`,
    'draft-edit': `
✏️ draft-edit - 编辑草稿

用法：node smtp.js draft-edit <draft-id> [options]

必填参数:
  <draft-id>            草稿 ID（如 DRAFT-20260329001234-G）

可选参数:
  --to <email>          更新收件人
  --subject <text>      更新主题
  --body <text>         更新正文
  --body-file <file>    从文件读取新正文
  --html <content>      更新 HTML 正文
  --html-file <file>    从文件读取 HTML 正文
  --cc <email>          更新抄送
  --bcc <email>         更新密送
  --attach <file>       更新附件（逗号分隔）
  --signature <name>    更新签名模板
  --language <lang>     更新语言
  --intent <type>       更新意图
  --notes <text>        更新备注
  --patch-file <file>   从 JSON 文件读取更新内容
  --no-approval         移除审批要求

示例:
  # 更新草稿正文
  node smtp.js draft-edit DRAFT-123 --body "New body content"
  
  # 从文件读取正文更新
  node smtp.js draft-edit DRAFT-123 --body-file updated-body.txt
  
  # 更新多个字段
  node smtp.js draft-edit DRAFT-123 --subject "New Subject" --to "new@example.com"
  
  # 从 JSON 文件读取完整更新
  node smtp.js draft-edit DRAFT-123 --patch-file updates.json
  
  # 添加附件
  node smtp.js draft-edit DRAFT-123 --attach "/path/to/file.pdf"
`,
    'send-status': `
📬 send-status - 查询发送状态

用法：node smtp.js send-status [query] [mode]

查询模式:
  （无参数）       显示最近 10 封发送记录
  <number>         显示指定数量的记录
  <index> index    按索引查询（0-based）
  <email> to       按收件人查询
  <subject> subject 按主题查询
  <message-id> messageId  按 Message-ID 查询

示例:
  # 查看最近 10 封发送记录
  node smtp.js send-status
  
  # 查看最近 N 封记录
  node smtp.js send-status 5
  
  # 按索引查询（0-based）
  node smtp.js send-status 0 index
  
  # 按收件人查询
  node smtp.js send-status "customer@example.com" to
  
  # 按主题查询
  node smtp.js send-status "Product Inquiry" subject
  
  # 按 Message-ID 查询
  node smtp.js send-status "<abc123@mail.server.com>" messageId
`,
    'reply': `
📤 reply - 回复邮件（自动回复全部）

用法：node smtp.js reply --message-id <UID> --body "回复内容" [options]

必填参数:
  --message-id <UID>    原邮件 UID（通过 imap.js check 获取）
  --body <text>         回复正文

可选参数:
  --subject <text>      自定义主题（默认：Re: 原主题）
  --signature <name>    使用签名模板
  --remove <email>      排除特定收件人（逗号分隔）
  --dry-run             预览但不发送

示例:
  # 回复邮件（自动回复全部）
  node smtp.js reply --message-id 12345 --body "Thanks for your email..."
  
  # 回复并自定义主题
  node smtp.js reply --message-id 12345 --subject "Re: Your Inquiry" --body "Thank you..."
  
  # 回复但排除特定收件人
  node smtp.js reply --message-id 12345 --body "Hi team..." --remove "noreply@example.com"
  
  # 预览回复（不发送）
  node smtp.js reply --message-id 12345 --body "Thanks!" --dry-run
`,
    'reply-all': `
📤 reply-all - 回复全部邮件

用法：node smtp.js reply-all --message-id <UID> --body "回复内容" [options]

必填参数:
  --message-id <UID>    原邮件 UID（通过 imap.js check 获取）
  --body <text>         回复正文

可选参数:
  --subject <text>      自定义主题（默认：Re: 原主题）
  --signature <name>    使用签名模板
  --remove <email>      排除特定收件人（逗号分隔）
  --dry-run             预览但不发送

示例:
  # 回复全部邮件
  node smtp.js reply-all --message-id 12345 --body "Thanks everyone..."
  
  # 回复全部并排除特定收件人
  node smtp.js reply-all --message-id 12345 --body "Hi team..." --remove "mailing-list@example.com"
  
  # 预览回复（不发送）
  node smtp.js reply-all --message-id 12345 --body "Thanks!" --dry-run
`,
    'forward': `
📤 forward - 转发邮件

用法：node smtp.js forward --message-id <UID> --to "email@example.com" [options]

必填参数:
  --message-id <UID>    原邮件 UID（通过 imap.js check 获取）
  --to <email>          转发目标邮箱

可选参数:
  --body <text>         转发说明（默认："Please see the forwarded email below."）
  --forward-attachments 转发原邮件附件
  --draft               保存为草稿（默认行为）
  --confirm-send        直接发送而不是保存草稿
  --dry-run             预览但不发送
  --mailbox <name>      原邮件所在文件夹（默认：INBOX）

示例:
  # 转发邮件（不含附件）
  node smtp.js forward --message-id 12345 --to "third@example.com" --body "Please see below..."
  
  # 转发邮件并附带原附件
  node smtp.js forward --message-id 12345 --to "colleague@example.com" --forward-attachments
  
  # 直接发送转发邮件（不走草稿）
  node smtp.js forward --message-id 12345 --to "manager@example.com" --confirm-send
  
  # 预览转发（不发送）
  node smtp.js forward --message-id 12345 --to "manager@example.com" --forward-attachments --dry-run
  
  # 从指定文件夹转发
  node smtp.js forward --message-id 67890 --to "team@example.com" --mailbox "Projects" --forward-attachments
`
  };

  if (helpMap[command]) {
    console.log(helpMap[command]);
  } else {
    console.error(`❌ 未知命令：${command}`);
    console.log('使用 node smtp.js -h 查看所有可用命令');
  }
}

function loadLog() {
  const LOG_FILE = path.join(WORKSPACE_DIR, 'mail-archive/sent/sent-log.json');

  if (fs.existsSync(LOG_FILE)) {
    try {
      return JSON.parse(fs.readFileSync(LOG_FILE, 'utf8'));
    } catch (err) {
      console.warn(`[rate-limit] Failed to parse log file: ${err.message}`);
      return [];
    }
  }
  return [];
}

// SMTP Transporter 单例（复用连接池）
let _transporter = null;

function getTransporter() {
  if (!_transporter) {
    _transporter = nodemailer.createTransport({
      pool: true,  // 启用连接池
      host: process.env.SMTP_HOST,
      port: parseInt(process.env.SMTP_PORT, 10) || 587,
      secure: process.env.SMTP_SECURE === 'true',
      auth: {
        user: process.env.SMTP_USER,
        pass: process.env.SMTP_PASS,
      },
      tls: {
        rejectUnauthorized: process.env.SMTP_REJECT_UNAUTHORIZED !== 'false',
      },
      maxConnections: 5,  // 最大并发连接数
    });
    console.log('[SMTP] Transporter created (connection pool enabled)');
  }
  return _transporter;
}

/**
 * @deprecated 使用 getTransporter() 代替，复用单例 transporter
 */
function createTransporter() {
  const config = {
    host: process.env.SMTP_HOST,
    port: parseInt(process.env.SMTP_PORT, 10) || 587,
    secure: process.env.SMTP_SECURE === 'true',
    auth: {
      user: process.env.SMTP_USER,
      pass: process.env.SMTP_PASS,
    },
    tls: {
      rejectUnauthorized: process.env.SMTP_REJECT_UNAUTHORIZED !== 'false',
    },
  };

  if (!config.host || !config.auth.user || !config.auth.pass) {
    throw new Error('Missing SMTP configuration. Please set SMTP_HOST, SMTP_USER, and SMTP_PASS in .env');
  }

  return nodemailer.createTransport(config);
}

async function buildMailOptions(options) {
  // Handle --reply-to: fetch original email and build quoted text
  let quotedText = '';
  let inReplyTo = undefined;
  let references = undefined;
  let replyAllRecipients = [];

  if (options.replyTo) {
    try {
      const originalEmail = await fetchEmail(options.replyTo);
      if (originalEmail) {
        // Set In-Reply-To header (points to immediate parent)
        inReplyTo = originalEmail.messageId || `<${options.replyTo}@mail>`;
        
        // Set References header (accumulates entire thread history)
        // Format: [ancestor-ids] [parent-id]
        if (originalEmail.references) {
          // Inherit parent's References + parent's Message-ID
          references = `${originalEmail.references} ${inReplyTo}`;
        } else {
          // First reply in thread: References = parent's Message-ID
          references = inReplyTo;
        }

        // Build quoted text
        const fromName = originalEmail.from || 'Sender';
        const fromDate = originalEmail.date ? new Date(originalEmail.date).toLocaleString() : 'Unknown date';
        const fromAddress = originalEmail.fromAddress || '';

        quotedText = `\n\n────────────────────────────────\nOn ${fromDate}, ${fromName} <${fromAddress}> wrote:\n\n${originalEmail.text || originalEmail.html || ''}`;

        // Auto "Reply All" - collect all recipients (original sender + To + Cc)
        const selfEmail = process.env.SMTP_USER;
        
        // Helper function to add recipient if valid and not self
        const addRecipient = (email) => {
          if (!email) return;
          const normalized = email.toLowerCase().trim();
          if (normalized === selfEmail?.toLowerCase()) return; // Exclude self
          if (!replyAllRecipients.some(r => r.toLowerCase() === normalized)) {
            replyAllRecipients.push(email);
          }
        };

        // 1. Add original sender (From)
        if (fromAddress) {
          addRecipient(fromAddress);
        }

        // 2. Add original To recipients
        if (originalEmail.to) {
          const toRecipients = originalEmail.to.split(',').map(r => r.trim());
          toRecipients.forEach(addRecipient);
        }

        // 3. Add original Cc recipients
        if (originalEmail.cc) {
          const ccRecipients = originalEmail.cc.split(',').map(r => r.trim());
          ccRecipients.forEach(addRecipient);
        }

        // 4. Handle --remove parameter: exclude specific addresses
        if (options.remove) {
          const removeList = options.remove.split(',').map(r => r.toLowerCase().trim());
          replyAllRecipients = replyAllRecipients.filter(r => 
            !removeList.some(remove => r.toLowerCase().includes(remove))
          );
        }
      }
    } catch (err) {
      console.error(`⚠️  Failed to fetch original email (UID: ${options.replyTo}): ${err.message}`);
    }
  }

  const mailOptions = {
    from: options.from || process.env.SMTP_FROM || process.env.SMTP_USER,
    to: options.to,
    // Auto "Reply All" unless explicitly overridden
    cc: options.cc !== undefined ? options.cc : (replyAllRecipients.length > 0 ? replyAllRecipients.join(',') : undefined),
    bcc: options.bcc || undefined,
    subject: options.subject || '(no subject)',
    text: options.text || undefined,
    html: options.html || undefined,
    attachments: options.attachments || [],
    headers: {
      'In-Reply-To': inReplyTo || undefined,
      'References': references || undefined,
    },
  };

  // Handle inline images (CID references)
  if (options.inlineImages && options.inlineImages.length > 0) {
    // Add inline images to attachments with cid property
    options.inlineImages.forEach(img => {
      mailOptions.attachments.push({
        filename: img.filename,
        path: img.path,
        cid: img.cid,
      });
    });
    
    // Validate HTML content contains matching cid references
    if (mailOptions.html) {
      const cidPattern = /cid:([^"'\s>]+)/g;
      const foundCids = new Set();
      let match;
      while ((match = cidPattern.exec(mailOptions.html)) !== null) {
        foundCids.add(match[1]);
      }
      
      const providedCids = new Set(options.inlineImages.map(img => img.cid));
      const missingCids = [...foundCids].filter(cid => !providedCids.has(cid));
      
      if (missingCids.length > 0) {
        console.error(`⚠️  Warning: HTML contains cid references without corresponding inline images: ${missingCids.join(', ')}`);
      }
      
      const unusedCids = [...providedCids].filter(cid => !foundCids.has(cid));
      if (unusedCids.length > 0) {
        console.error(`⚠️  Warning: Inline images provided but not used in HTML: ${unusedCids.join(', ')}`);
      }
    }
  }

  if (!mailOptions.text && !mailOptions.html) {
    mailOptions.text = options.body || '';
  }

  // Append quoted text if present
  if (quotedText) {
    // Always append to text version (for proper plain text quoting)
    if (mailOptions.text) {
      mailOptions.text += quotedText;
    }
    // For HTML, use properly formatted block
    if (mailOptions.html) {
      // Strip HTML tags from quoted text for clean display
      const plainQuoted = quotedText.replace(/<[^>]*>/g, '');
      mailOptions.html += `<br><br><div style="border-left: 2px solid #ccc; padding-left: 15px; margin-top: 20px; color: #666; font-size: 13px;"><p style="margin: 0 0 10px 0; font-weight: bold; color: #999;">────────────────────────────────</p><p style="margin: 0; white-space: pre-wrap;">${plainQuoted}</p></div>`;
    }
  }

  // Add signature
  if (options.signature && options.signatureHtml) {
    if (mailOptions.html) {
      mailOptions.html += options.signatureHtml;
    } else if (mailOptions.text) {
      mailOptions.html = mailOptions.text.replace(/\n/g, '<br>') + options.signatureHtml;
      delete mailOptions.text;
    } else {
      mailOptions.html = options.signatureHtml;
    }
  }

  return mailOptions;
}

async function sendEmail(options) {
  const isDryRun = Boolean(options.dryRun || options['dry-run']);
  const isConfirmSend = Boolean(options.confirmSend || options['confirm-send']);
  const mailOptions = await buildMailOptions(options);

  // P0-2: Draft-first behavior - default to saving draft unless --confirm-send is provided
  if (!isDryRun && !isConfirmSend) {
    // Save as draft instead of sending
    const { saveDraft } = require('./drafts');
    const draftData = {
      to: mailOptions.to,
      cc: mailOptions.cc,
      bcc: mailOptions.bcc,
      subject: mailOptions.subject,
      body: mailOptions.text || '',
      html: mailOptions.html || null,
      attachments: mailOptions.attachments || [],
      signature: options.signature,
      language: options.language || 'en',
      intent: options.intent,
      requires_human_approval: true,
      notes: 'Auto-saved draft from send command (draft-first mode)',
    };
    const draftResult = saveDraft(draftData);
    return {
      success: true,
      draft: true,
      draft_id: draftResult.draft_id,
      message: '草稿已保存，使用 --confirm-send 参数实际发送',
      logEntry: recordSentEmail(mailOptions, { success: true, messageId: null, draft: true }),
    };
  }

  if (!isDryRun && isConfirmSend) {
    const transporter = getTransporter();

    try {
      await transporter.verify();
      console.error('SMTP server is ready to send');
    } catch (err) {
      throw new Error(`SMTP connection failed: ${err.message}`);
    }

    const rateLimit = parseInt(process.env.SMTP_RATE_LIMIT, 10) || 50;
    const oneHourAgo = new Date(Date.now() - 60 * 60 * 1000).toISOString();
    // Filter by numeric status code 4 (成功) or legacy string 'sent'
    const recentLog = loadLog().filter(entry => entry.timestamp > oneHourAgo && (entry.status === 4 || entry.status === 'sent'));

    if (recentLog.length >= rateLimit) {
      throw new Error(
        `Rate limit exceeded: ${recentLog.length}/${rateLimit} emails sent in the last hour. ` +
        `Please wait before sending more emails. (SMTP_RATE_LIMIT=${rateLimit})`
      );
    }

    console.error(`[Rate Limit] ${recentLog.length}/${rateLimit} emails sent in last hour - OK to send`);

    const info = await transporter.sendMail(mailOptions);
    const logEntry = recordSentEmail(mailOptions, { success: true, messageId: info.messageId });

    // Auto-check delivery status after sending (wait 2 seconds for server processing)
    await new Promise(resolve => setTimeout(resolve, 2000));

    // Query the log to confirm delivery status
    const statusEntry = getStatus(info.messageId, 'messageId');
    const confirmedDeliveryStatus = statusEntry ? {
      status: statusEntry.status || 4,  // 4=成功
      status_text: statusEntry.status_text || '成功',
      messageId: info.messageId,
      acceptedByServer: true,
      confirmedAt: new Date().toISOString(),
      deliveryNote: statusEntry.deliveryNote || 'Email accepted by SMTP server',
    } : {
      status: 4,  // 4=成功
      status_text: '成功',
      messageId: info.messageId,
      acceptedByServer: true,
      confirmedAt: new Date().toISOString(),
      deliveryNote: 'Email accepted by SMTP server',
    };

    // Update log entry with confirmed status
    const { updateLogEntry } = require('./send-log');
    if (updateLogEntry) {
      try {
        updateLogEntry(info.messageId, { deliveryStatus: confirmedDeliveryStatus });
      } catch (err) {
        console.error(`[send-email] Failed to update delivery status: ${err.message}`);
      }
    }

    return {
      success: true,
      messageId: info.messageId,
      response: info.response,
      to: mailOptions.to,
      status: confirmedDeliveryStatus,
      logEntry: {
        timestamp: logEntry.timestamp,
        from: logEntry.from,
        subject: logEntry.subject,
      },
    };
  }

  console.error('\n🔍 DRY-RUN MODE - Email NOT sent\n');
  console.error('═══════════════════════════════════════════════════════════');
  console.error('From:', mailOptions.from);
  console.error('To:', mailOptions.to);
  if (mailOptions.cc) console.error('CC:', mailOptions.cc);
  if (mailOptions.bcc) console.error('BCC:', mailOptions.bcc);
  console.error('Subject:', mailOptions.subject);
  console.error('───────────────────────────────────────────────────────────');
  console.error('Body (text):', mailOptions.text ? mailOptions.text.substring(0, 500) + (mailOptions.text.length > 500 ? '...' : '') : '(none)');
  if (mailOptions.html) {
    console.error('Body (html):', mailOptions.html.substring(0, 500) + (mailOptions.html.length > 500 ? '...' : ''));
  }
  if (mailOptions.attachments && mailOptions.attachments.length > 0) {
    console.error('───────────────────────────────────────────────────────────');
    console.error('Attachments:');
    mailOptions.attachments.forEach((att, i) => {
      console.error(`  ${i + 1}. ${att.filename || att.path}`);
    });
  }
  console.error('═══════════════════════════════════════════════════════════\n');

  const logEntry = recordSentEmail(mailOptions, { success: true, messageId: null });

  return {
    success: true,
    dryRun: true,
    preview: {
      from: mailOptions.from,
      to: mailOptions.to,
      cc: mailOptions.cc,
      bcc: mailOptions.bcc,
      subject: mailOptions.subject,
      text: mailOptions.text,
      html: mailOptions.html,
      attachments: mailOptions.attachments.map(att => att.filename || att.path),
    },
    status: {
      status: 'dry_run',
      messageId: null,
      acceptedByServer: false,
      timestamp: new Date().toISOString(),
      note: 'Dry-run mode - email not actually sent',
    },
    logEntry: {
      timestamp: logEntry.timestamp,
      from: logEntry.from,
      subject: logEntry.subject,
    },
  };
}

function renderSignature(sigData) {
  // Replace placeholder [Your Name] with actual sender name
  const senderName = process.env.SMTP_SENDER_NAME || 'Simon Lee';
  const nameValue = sigData.name_field === '[Your Name]' ? senderName : sigData.name_field;
  
  return `
<br>
<div style="font-family: Arial, sans-serif; font-size: 14px; line-height: 1.6; color: #333;">
  <p style="margin: 0;">${sigData.greeting}</p>
  <p style="margin: 5px 0;"><strong>${nameValue}</strong><br>
  ${sigData.title}<br>
  ${sigData.company}</p>
  <p style="margin: 5px 0; font-size: 12px; color: #666;">
    📍 ${sigData.address_cn}<br>
    📍 ${sigData.address_vn}<br>
    📧 ${sigData.email} | 📞 ${sigData.phone}<br>
    🌐 ${sigData.website}</p>
  <p style="margin: 10px 0 0; padding-top: 10px; border-top: 1px solid #ddd; font-size: 12px; color: #999;">
    ${sigData.tagline}
  </p>
</div>
  `.trim();
}

function readAttachment(filePath) {
  const realPath = validateReadPath(filePath);
  if (!fs.existsSync(realPath)) {
    throw new Error(`Attachment file not found: ${filePath}`);
  }
  return {
    filename: path.basename(realPath),
    path: realPath,
  };
}

function ensureScheduledDir() {
  if (!fs.existsSync(SCHEDULED_DIR)) {
    fs.mkdirSync(SCHEDULED_DIR, { recursive: true });
  }
}

function generateScheduleId() {
  return `sched-${Date.now()}-${Math.random().toString(36).slice(2, 10)}`;
}

function parseSendAt(input) {
  if (!input || typeof input !== 'string') {
    throw new Error('Missing required option: --send-at "YYYY-MM-DD HH:mm"');
  }

  const trimmed = input.trim();
  const match = trimmed.match(/^(\d{4})-(\d{2})-(\d{2})\s+(\d{2}):(\d{2})(?::(\d{2}))?$/);
  if (!match) {
    throw new Error('Invalid --send-at format. Expected "YYYY-MM-DD HH:mm"');
  }

  const [, year, month, day, hour, minute, second = '0'] = match;
  const date = new Date(
    Number(year),
    Number(month) - 1,
    Number(day),
    Number(hour),
    Number(minute),
    Number(second),
    0
  );

  if (Number.isNaN(date.getTime())) {
    throw new Error(`Invalid --send-at value: ${input}`);
  }

  return date;
}

function serializeMailOptions(options) {
  return {
    from: options.from,
    to: options.to,
    cc: options.cc,
    bcc: options.bcc,
    subject: options.subject,
    text: options.text,
    html: options.html,
    body: options.body,
    signature: options.signature,
    signatureHtml: options.signatureHtml,
    dryRun: Boolean(options.dryRun || options['dry-run']),
    attachments: (options.attachments || []).map(att => ({
      filename: att.filename,
      path: att.path,
    })),
  };
}

function writeScheduleRecord(record) {
  ensureScheduledDir();
  const filePath = path.join(SCHEDULED_DIR, `${record.id}.json`);
  fs.writeFileSync(filePath, JSON.stringify(record, null, 2), 'utf8');
  return filePath;
}

function loadScheduleRecord(filePath) {
  return JSON.parse(fs.readFileSync(filePath, 'utf8'));
}

function saveScheduleRecord(filePath, record) {
  fs.writeFileSync(filePath, JSON.stringify(record, null, 2), 'utf8');
}

async function processScheduledFile(filePath) {
  const record = loadScheduleRecord(filePath);

  if (record.status !== 'pending') {
    return {
      skipped: true,
      reason: `Schedule already ${record.status}`,
      id: record.id,
      file: filePath,
    };
  }

  record.status = 'sending';
  record.processingStartedAt = new Date().toISOString();
  saveScheduleRecord(filePath, record);

  try {
    const result = await sendEmail(record.mailOptions);
    record.status = 'sent';
    record.sentAt = new Date().toISOString();
    record.result = result;
    saveScheduleRecord(filePath, record);

    return {
      id: record.id,
      file: filePath,
      status: record.status,
      result,
    };
  } catch (err) {
    record.status = 'failed';
    record.failedAt = new Date().toISOString();
    record.error = err.message;
    saveScheduleRecord(filePath, record);
    throw err;
  }
}

async function scheduleEmail(options, sendAtInput) {
  const sendAt = parseSendAt(sendAtInput);
  const now = Date.now();
  const delayMs = sendAt.getTime() - now;

  const record = {
    id: generateScheduleId(),
    createdAt: new Date().toISOString(),
    sendAt: sendAt.toISOString(),
    requestedSendAt: sendAtInput,
    status: 'pending',
    mailOptions: serializeMailOptions(options),
  };

  const filePath = writeScheduleRecord(record);

  if (delayMs <= 0) {
    const result = await processScheduledFile(filePath);
    return {
      success: true,
      scheduled: true,
      immediate: true,
      id: record.id,
      file: filePath,
      sendAt: record.sendAt,
      result,
    };
  }

  console.error(`⏰ Scheduled email ${record.id} for ${record.sendAt} (${Math.round(delayMs / 1000)}s later)`);

  await new Promise((resolve, reject) => {
    setTimeout(async () => {
      try {
        await processScheduledFile(filePath);
        resolve();
      } catch (err) {
        reject(err);
      }
    }, delayMs);
  });

  const finalRecord = loadScheduleRecord(filePath);
  return {
    success: true,
    scheduled: true,
    completed: true,
    id: record.id,
    file: filePath,
    sendAt: finalRecord.sendAt,
    status: finalRecord.status,
    result: finalRecord.result,
  };
}

function listScheduledEmails() {
  ensureScheduledDir();
  return fs.readdirSync(SCHEDULED_DIR)
    .filter(name => name.endsWith('.json'))
    .sort()
    .map(name => {
      const filePath = path.join(SCHEDULED_DIR, name);
      const record = loadScheduleRecord(filePath);
      return {
        id: record.id,
        file: filePath,
        status: record.status,
        sendAt: record.sendAt,
        to: record.mailOptions?.to,
        subject: record.mailOptions?.subject,
      };
    });
}

async function sendDueScheduledEmails() {
  const now = Date.now();
  const scheduled = listScheduledEmails();
  const due = scheduled.filter(item => item.status === 'pending' && new Date(item.sendAt).getTime() <= now);
  const results = [];

  for (const item of due) {
    try {
      const result = await processScheduledFile(item.file);
      results.push({ success: true, ...result });
    } catch (err) {
      results.push({ success: false, id: item.id, file: item.file, error: err.message });
    }
  }

  return {
    success: true,
    processed: results.length,
    results,
  };
}

async function prepareSendOptions(options) {
  if (!options.to) {
    throw new Error('Missing required option: --to <email>');
  }
  if (!options.subject && !options['subject-file']) {
    throw new Error('Missing required option: --subject <text> or --subject-file <file>');
  }

  if (options['subject-file']) {
    validateReadPath(options['subject-file']);
    options.subject = fs.readFileSync(options['subject-file'], 'utf8').trim();
  }

  if (options['body-file']) {
    validateReadPath(options['body-file']);
    const content = fs.readFileSync(options['body-file'], 'utf8');
    if (options['body-file'].endsWith('.html') || options.html) {
      options.html = content;
      delete options.text;
    } else {
      options.text = content;
      delete options.html;
    }
  } else if (options['html-file']) {
    validateReadPath(options['html-file']);
    options.html = fs.readFileSync(options['html-file'], 'utf8');
    delete options.text;
  } else if (options.body) {
    if (options.html === true || options.html === 'true') {
      options.html = options.body;
      delete options.text;
    } else {
      options.text = options.body;
      delete options.html;
    }
  }

  if (options.attach) {
    const attachFiles = options.attach.split(',').map(f => f.trim()).filter(Boolean);
    options.attachments = attachFiles.map(f => readAttachment(f));
    console.log(`📎 已添加 ${options.attachments.length} 个附件:`);
    options.attachments.forEach(att => console.log(`   - ${att.filename}`));
  }

  // Handle --inline parameter for embedded images (CID references)
  if (options.inline) {
    // Check mutual exclusion with --plain-text
    if (options['plain-text']) {
      throw new Error('❌ --plain-text and --inline are mutually exclusive. Inline images require HTML content.');
    }
    
    try {
      // Parse JSON array: '[{"cid":"abc123","path":"./logo.png"}]'
      const inlineImages = JSON.parse(options.inline);
      if (!Array.isArray(inlineImages)) {
        throw new Error('--inline must be a JSON array of objects with "cid" and "path" properties');
      }
      
      options.inlineImages = inlineImages.map(img => {
        if (!img.cid || !img.path) {
          throw new Error(`Each inline image must have "cid" and "path" properties: ${JSON.stringify(img)}`);
        }
        const realPath = validateReadPath(img.path);
        if (!fs.existsSync(realPath)) {
          throw new Error(`Inline image file not found: ${img.path}`);
        }
        return {
          cid: img.cid,
          filename: path.basename(realPath),
          path: realPath,
        };
      });
      
      console.log(`🖼️  已添加 ${options.inlineImages.length} 个内嵌图片:`);
      options.inlineImages.forEach(img => console.log(`   - CID: ${img.cid}, File: ${img.filename}`));
      
      // Ensure HTML mode is enabled for inline images
      options.html = options.html || true;
    } catch (err) {
      if (err instanceof SyntaxError) {
        throw new Error(`Invalid --inline JSON format: ${options.inline}. Expected format: '[{"cid":"abc123","path":"./logo.png"}]'`);
      }
      throw err;
    }
  }

  if (options.signature) {
    const signaturePath = path.resolve(__dirname, `../signatures/signature-${options.signature}.json`);
    if (fs.existsSync(signaturePath)) {
      const sigData = JSON.parse(fs.readFileSync(signaturePath, 'utf8'));
      options.signatureHtml = renderSignature(sigData);
      console.log(`📝 已加载签名模板：${options.signature}`);
    } else {
      console.error(`⚠️  签名模板不存在：${signaturePath}`);
    }
  }

  // Handle --plain-text parameter: force plain text mode, ignore HTML
  if (options['plain-text']) {
    if (options.html) {
      console.log('⚠️  --plain-text specified, HTML content will be converted to plain text');
      delete options.html;
    }
    if (options.body && !options.text) {
      options.text = options.body;
    }
    console.log('📝 强制纯文本模式已启用');
  }

  // Normalize --reply-to parameter
  if (options['reply-to']) {
    options.replyTo = options['reply-to'];
  }

  return options;
}

async function testConnection() {
  const transporter = getTransporter();

  try {
    await transporter.verify();
    const info = await transporter.sendMail({
      from: process.env.SMTP_FROM || process.env.SMTP_USER,
      to: process.env.SMTP_USER,
      subject: 'SMTP Connection Test',
      text: 'This is a test email from the IMAP/SMTP email skill.',
      html: '<p>This is a <strong>test email</strong> from the IMAP/SMTP email skill.</p>',
    });

    return {
      success: true,
      message: 'SMTP connection successful',
      messageId: info.messageId,
    };
  } catch (err) {
    throw new Error(`SMTP test failed: ${err.message}`);
  }
}

async function interactiveMode() {
  const prompts = require('prompts');

  console.log('\n📧 SMTP Email Interactive Mode\n');
  console.log('Follow the prompts to configure and send an email.\n');

  // Step 1: Recipient
  const toPrompt = await prompts({
    type: 'text',
    name: 'to',
    message: 'Recipient email (to):',
    validate: value => value && value.includes('@') ? true : 'Please enter a valid email address',
  });

  if (!toPrompt.to) {
    console.log('Cancelled.');
    return;
  }

  // Step 2: CC (optional)
  const ccPrompt = await prompts({
    type: 'text',
    name: 'cc',
    message: 'CC email(s) (optional, comma-separated):',
  });

  // Step 3: Subject
  const subjectPrompt = await prompts({
    type: 'text',
    name: 'subject',
    message: 'Email subject:',
    validate: value => value ? true : 'Subject is required',
  });

  if (!subjectPrompt.subject) {
    console.log('Cancelled.');
    return;
  }

  // Step 4: Content type
  const typePrompt = await prompts({
    type: 'select',
    name: 'contentType',
    message: 'Content type:',
    choices: [
      { title: 'Plain Text', value: 'text' },
      { title: 'HTML', value: 'html' },
    ],
  });

  // Step 5: Body content
  const bodyPrompt = await prompts({
    type: 'text',
    name: 'body',
    message: `Enter email body (${typePrompt.contentType}):`,
    validate: value => value ? true : 'Body is required',
  });

  if (!bodyPrompt.body) {
    console.log('Cancelled.');
    return;
  }

  // Step 6: Attachments (optional)
  const attachPrompt = await prompts({
    type: 'text',
    name: 'attachments',
    message: 'Attachments (optional, comma-separated paths):',
  });

  // Step 7: Signature (optional)
  const sigPrompt = await prompts({
    type: 'text',
    name: 'signature',
    message: 'Signature template name (optional, e.g., en-sales):',
  });

  // Step 8: Confirm
  const confirmPrompt = await prompts({
    type: 'confirm',
    name: 'send',
    message: 'Send this email?',
    initial: true,
  });

  if (!confirmPrompt.send) {
    console.log('Cancelled.');
    return;
  }

  // Build options
  const options = {
    to: toPrompt.to,
    cc: ccPrompt.cc || undefined,
    subject: subjectPrompt.subject,
    [typePrompt.contentType]: bodyPrompt.body,
    signature: sigPrompt.signature || undefined,
  };

  if (attachPrompt.attachments) {
    options.attach = attachPrompt.attachments;
  }

  // Send email
  try {
    const prepared = await prepareSendOptions(options);
    const result = await sendEmail(prepared);
    console.log('\n✅ Email sent successfully!');
    console.log(JSON.stringify(result, null, 2));
  } catch (err) {
    console.error('\n❌ Failed to send email:', err.message);
    process.exit(1);
  }
}

async function main() {
  const { command, options, positional } = parseArgs();

  // 检查帮助参数
  if (command === '-h' || command === '--help' || options.h || options.help) {
    if (command && command !== '-h' && command !== '--help') {
      showCommandHelp(command);
    } else {
      showGlobalHelp();
    }
    return;
  }

  // 无参数时显示全局帮助
  if (process.argv.length === 2) {
    showGlobalHelp();
    return;
  }

  try {
    let result;

    switch (command) {
      case 'send': {
        const prepared = await prepareSendOptions(options);
        if (prepared['send-at']) {
          result = await scheduleEmail(prepared, prepared['send-at']);
        } else {
          result = await sendEmail(prepared);
        }
        break;
      }

      case 'send-due':
        result = await sendDueScheduledEmails();
        break;

      case 'list-scheduled':
        result = {
          success: true,
          scheduledDir: SCHEDULED_DIR,
          items: listScheduledEmails(),
        };
        break;

      case 'test':
        result = await testConnection();
        break;

      case 'list-signatures': {
        const signaturesDir = path.resolve(__dirname, '../signatures');
        if (!fs.existsSync(signaturesDir)) {
          console.error('❌ 签名目录不存在:', signaturesDir);
          process.exit(1);
        }

        const files = fs.readdirSync(signaturesDir).filter(f => f.endsWith('.json'));
        if (files.length === 0) {
          console.log('📭 暂无签名模板');
          process.exit(0);
        }

        console.log('\n📝 可用签名模板:\n');
        files.forEach(file => {
          const sigData = JSON.parse(fs.readFileSync(path.join(signaturesDir, file), 'utf8'));
          const name = file.replace('signature-', '').replace('.json', '');
          console.log(`  - ${name} (${sigData.language || 'unknown'} / ${sigData.role || 'general'})`);
        });
        console.log('');
        return;
      }

      case 'show-signature': {
        const sigName = positional[0];
        if (!sigName) {
          console.error('❌ 缺少参数：签名名称');
          console.error('用法：show-signature <name>');
          console.error('示例：show-signature en-sales');
          process.exit(1);
        }

        const signaturePath = path.resolve(__dirname, `../signatures/signature-${sigName}.json`);
        if (!fs.existsSync(signaturePath)) {
          console.error(`❌ 签名模板不存在：${signaturePath}`);
          console.error('可用签名：运行 list-signatures 查看所有模板');
          process.exit(1);
        }

        const sigData = JSON.parse(fs.readFileSync(signaturePath, 'utf8'));
        console.log('\n📝 签名模板详情:\n');
        console.log('名称:', sigName);
        console.log('语言:', sigData.language || '未指定');
        console.log('角色:', sigData.role || '未指定');
        console.log('─────────────────────────────────────────');
        console.log('问候语:', sigData.greeting);
        console.log('姓名:', sigData.name_field);
        console.log('职位:', sigData.title);
        console.log('公司:', sigData.company);
        console.log('邮箱:', sigData.email);
        console.log('电话:', sigData.phone);
        console.log('网站:', sigData.website);
        console.log('地址 (中国):', sigData.address_cn);
        console.log('地址 (越南):', sigData.address_vn);
        console.log('标语:', sigData.tagline);
        console.log('');
        return;
      }

      case 'interactive':
        await interactiveMode();
        return;

      // Draft commands
      case 'draft':
      case 'save-draft': {
        const { saveDraft } = require('./drafts');
        
        // Build draft data from options
        const draftData = {
          to: options.to,
          cc: options.cc,
          bcc: options.bcc,
          subject: options.subject,
          body: options.body,
          html: options.html,
          signature: options.signature,
          language: options.language || 'en',
          intent: options.intent,
          template_used: options.template,
          requires_human_approval: options['no-approval'] !== true,
          notes: options.notes,
        };
        
        // Load body from file if specified
        if (options['body-file']) {
          validateReadPath(options['body-file']);
          draftData.body = fs.readFileSync(options['body-file'], 'utf8');
        }
        
        // Handle attachments
        if (options.attach) {
          const attachFiles = options.attach.split(',').map(f => f.trim()).filter(Boolean);
          draftData.attachments = attachFiles.map(f => ({
            filename: path.basename(f),
            path: validateReadPath(f),
          }));
        }
        
        // Load from file if specified
        if (options.file) {
          validateReadPath(options.file);
          const fileData = JSON.parse(fs.readFileSync(options.file, 'utf8'));
          Object.assign(draftData, fileData);
        }
        
        result = saveDraft(draftData);
        break;
      }

      case 'send-draft': {
        const { sendDraft } = require('./drafts');
        const draftId = positional[0];
        
        if (!draftId) {
          console.error('❌ Missing draft ID');
          console.error('Usage: send-draft <draft-id> [--confirm-send] [--dry-run]');
          process.exit(1);
        }
        
        result = await sendDraft(draftId, {
          confirmSend: options['confirm-send'],
          dryRun: options['dry-run'],
          archive: options.archive,
        });
        break;
      }

      case 'list-drafts': {
        const { listDrafts } = require('./drafts');
        
        const drafts = listDrafts({
          intent: options.intent,
          language: options.language,
          onlyApproval: options['only-approval'],
        });
        
        if (options.json) {
          console.log(JSON.stringify(drafts, null, 2));
        } else {
          console.log('\n📝 Drafts:\n');
          if (drafts.length === 0) {
            console.log('  (no drafts)');
          } else {
            drafts.forEach((d, i) => {
              const approvalFlag = d.requires_human_approval ? '⚠️ ' : '✅ ';
              console.log(`  ${i + 1}. ${approvalFlag}${d.draft_id}`);
              console.log(`     To: ${d.to}`);
              console.log(`     Subject: ${d.subject}`);
              console.log(`     Intent: ${d.intent || 'general'} | Lang: ${d.language}`);
              console.log(`     Created: ${d.created_at}`);
              console.log('');
            });
          }
          console.log(`Total: ${drafts.length} draft(s)\n`);
        }
        return;
      }

      case 'show-draft': {
        const { loadDraft } = require('./drafts');
        const draftId = positional[0];
        
        if (!draftId) {
          console.error('❌ Missing draft ID');
          console.error('Usage: show-draft <draft-id>');
          process.exit(1);
        }
        
        const draft = loadDraft(draftId);
        if (!draft) {
          console.error(`❌ Draft not found: ${draftId}`);
          process.exit(1);
        }
        
        if (options.json) {
          console.log(JSON.stringify(draft, null, 2));
        } else {
          console.log('\n📝 Draft Details:\n');
          console.log('ID:', draft.draft_id);
          console.log('To:', draft.to);
          if (draft.cc) console.log('CC:', draft.cc);
          console.log('Subject:', draft.subject);
          console.log('Language:', draft.language);
          console.log('Intent:', draft.intent);
          console.log('Requires Approval:', draft.requires_human_approval ? 'Yes ⚠️' : 'No');
          console.log('Created:', draft.created_at);
          console.log('Updated:', draft.updated_at);
          console.log('─────────────────────────────────────────');
          console.log('Body:');
          console.log(draft.body || draft.html);
          console.log('');
        }
        return;
      }

      case 'delete-draft': {
        const { deleteDraft } = require('./drafts');
        const draftId = positional[0];
        
        if (!draftId) {
          console.error('❌ Missing draft ID');
          console.error('Usage: delete-draft <draft-id>');
          process.exit(1);
        }
        
        result = deleteDraft(draftId);
        break;
      }

      case 'draft-edit':
      case 'edit-draft': {
        const { editDraft } = require('./drafts');
        const draftId = positional[0];
        
        if (!draftId) {
          console.error('❌ Missing draft ID');
          console.error('Usage: draft-edit <draft-id> [--to <email>] [--subject <text>] [--body <text>] [--patch-file <file>]');
          process.exit(1);
        }
        
        // Build updates from command-line options
        const updates = {};
        
        // Support --patch-file for JSON patch
        if (options['patch-file']) {
          validateReadPath(options['patch-file']);
          const patchData = JSON.parse(fs.readFileSync(options['patch-file'], 'utf8'));
          Object.assign(updates, patchData);
        }
        
        // Support individual field updates
        if (options.to) updates.to = options.to;
        if (options.subject) updates.subject = options.subject;
        if (options.body) updates.body = options.body;
        if (options.cc) updates.cc = options.cc;
        if (options.bcc) updates.bcc = options.bcc;
        if (options.html) updates.html = options.html;
        if (options.signature) updates.signature = options.signature;
        if (options.language) updates.language = options.language;
        if (options.intent) updates.intent = options.intent;
        if (options.notes) updates.notes = options.notes;
        if (options['no-approval']) updates.requires_human_approval = false;
        
        // Handle --body-file
        if (options['body-file']) {
          validateReadPath(options['body-file']);
          updates.body = fs.readFileSync(options['body-file'], 'utf8');
        }
        
        // Handle --html-file
        if (options['html-file']) {
          validateReadPath(options['html-file']);
          updates.html = fs.readFileSync(options['html-file'], 'utf8');
        }
        
        // Handle attachments update
        if (options.attach) {
          const attachFiles = options.attach.split(',').map(f => f.trim()).filter(Boolean);
          updates.attachments = attachFiles.map(f => ({
            filename: path.basename(f),
            path: validateReadPath(f),
          }));
        }
        
        if (Object.keys(updates).length === 0) {
          console.error('❌ No updates provided');
          console.error('Usage: draft-edit <draft-id> [--to <email>] [--subject <text>] [--body <text>] [--patch-file <file>]');
          process.exit(1);
        }
        
        result = editDraft(draftId, updates);
        break;
      }

      case 'send-status':
      case 'status': {
        const identifier = positional[0];
        const field = positional[1] || 'messageId';
        
        if (!identifier) {
          // No identifier provided, show recent statuses
          const statusLimit = 10;
          const { getAllRecentStatus } = require('./send-log');
          const statuses = getAllRecentStatus(statusLimit);
          console.log(JSON.stringify({
            success: true,
            count: statuses.length,
            statuses,
          }, null, 2));
        } else if (field === 'messageId' && !isNaN(parseInt(identifier))) {
          // If only a number is provided, treat it as limit for recent statuses
          const statusLimit = parseInt(identifier);
          const { getAllRecentStatus } = require('./send-log');
          const statuses = getAllRecentStatus(statusLimit);
          console.log(JSON.stringify({
            success: true,
            count: statuses.length,
            statuses,
          }, null, 2));
        } else {
          const status = getStatus(identifier, field);
          if (!status) {
            console.error(`Email not found: ${identifier} (field: ${field})`);
            process.exit(1);
          }
          console.log(JSON.stringify({
            success: true,
            status,
          }, null, 2));
        }
        return;
      }

      case 'forward': {
        const { forwardEmail } = require('./forward');
        
        if (!options['message-id']) {
          console.error('❌ Missing required parameter: --message-id <UID>');
          console.error('Usage: node smtp.js forward --message-id <UID> --to "email@example.com" [--body "Forward note"] [--forward-attachments]');
          process.exit(1);
        }
        
        if (!options.to) {
          console.error('❌ Missing required parameter: --to <email>');
          console.error('Usage: node smtp.js forward --message-id <UID> --to "email@example.com" [--body "Forward note"] [--forward-attachments]');
          process.exit(1);
        }
        
        result = await forwardEmail({
          uid: options['message-id'],
          to: options.to,
          cc: options.cc,
          bcc: options.bcc,
          body: options.body || 'Please see the forwarded email below.',
          signature: options.signature,
          forwardAttachments: options['forward-attachments'] === true || options['forward-attachments'] === 'true',
          draft: options.draft !== 'false' && !(options['confirm-send'] === true || options['confirm-send'] === 'true'),
          confirmSend: options['confirm-send'] === true || options['confirm-send'] === 'true',
          dryRun: options['dry-run'] === true || options['dry-run'] === 'true',
          mailbox: options.mailbox,
        });
        break;
      }

      // Reply commands (aligned with lark-mail style)
      case 'reply': {
        if (!options['message-id']) {
          console.error('❌ Missing required parameter: --message-id <UID>');
          console.error('Usage: node smtp.js reply --message-id <UID> --body "回复内容" [--signature <name>] [--remove <email>]');
          process.exit(1);
        }
        
        if (!options.body && !options['body-file']) {
          console.error('❌ Missing required parameter: --body <text> or --body-file <file>');
          console.error('Usage: node smtp.js reply --message-id <UID> --body "回复内容"');
          process.exit(1);
        }
        
        // Build reply options
        const replyOptions = {
          to: options.to || 'placeholder@reply.local', // Will be overridden by reply-to logic
          subject: options.subject || `Re: `,
          body: options.body || '',
          signature: options.signature,
          remove: options.remove,
          dryRun: options['dry-run'],
        };
        
        // Load body from file if specified
        if (options['body-file']) {
          validateReadPath(options['body-file']);
          replyOptions.body = fs.readFileSync(options['body-file'], 'utf8');
        }
        
        // Use send command with reply-to parameter
        replyOptions['reply-to'] = options['message-id'];
        
        const prepared = await prepareSendOptions(replyOptions);
        result = await sendEmail(prepared);
        break;
      }

      case 'reply-all': {
        if (!options['message-id']) {
          console.error('❌ Missing required parameter: --message-id <UID>');
          console.error('Usage: node smtp.js reply-all --message-id <UID> --body "回复内容" [--signature <name>] [--remove <email>]');
          process.exit(1);
        }
        
        if (!options.body && !options['body-file']) {
          console.error('❌ Missing required parameter: --body <text> or --body-file <file>');
          console.error('Usage: node smtp.js reply-all --message-id <UID> --body "回复内容"');
          process.exit(1);
        }
        
        // Build reply-all options (same as reply, but explicitly enables auto-CC)
        const replyOptions = {
          to: options.to || 'placeholder@reply.local',
          subject: options.subject || `Re: `,
          body: options.body || '',
          signature: options.signature,
          remove: options.remove,
          dryRun: options['dry-run'],
        };
        
        // Load body from file if specified
        if (options['body-file']) {
          validateReadPath(options['body-file']);
          replyOptions.body = fs.readFileSync(options['body-file'], 'utf8');
        }
        
        // Use send command with reply-to parameter
        replyOptions['reply-to'] = options['message-id'];
        
        const prepared = await prepareSendOptions(replyOptions);
        result = await sendEmail(prepared);
        break;
      }

      // Draft aliases (for backward compatibility)
      case 'draft-create':
      case 'create-draft': {
        // Alias for 'draft' command
        const { saveDraft } = require('./drafts');
        
        const draftData = {
          to: options.to,
          cc: options.cc,
          bcc: options.bcc,
          subject: options.subject,
          body: options.body,
          html: options.html,
          signature: options.signature,
          language: options.language || 'en',
          intent: options.intent,
          template_used: options.template,
          requires_human_approval: options['no-approval'] !== true,
          notes: options.notes,
        };
        
        if (options['body-file']) {
          validateReadPath(options['body-file']);
          draftData.body = fs.readFileSync(options['body-file'], 'utf8');
        }
        
        if (options.attach) {
          const attachFiles = options.attach.split(',').map(f => f.trim()).filter(Boolean);
          draftData.attachments = attachFiles.map(f => ({
            filename: path.basename(f),
            path: validateReadPath(f),
          }));
        }
        
        if (options.file) {
          validateReadPath(options.file);
          const fileData = JSON.parse(fs.readFileSync(options.file, 'utf8'));
          Object.assign(draftData, fileData);
        }
        
        result = saveDraft(draftData);
        break;
      }

      case 'draft-send': {
        // Alias for 'send-draft' command
        const { sendDraft } = require('./drafts');
        const draftId = positional[0];
        
        if (!draftId) {
          console.error('❌ Missing draft ID');
          console.error('Usage: draft-send <draft-id> [--confirm-send] [--dry-run]');
          process.exit(1);
        }
        
        result = await sendDraft(draftId, {
          confirmSend: options['confirm-send'],
          dryRun: options['dry-run'],
          archive: options.archive,
        });
        break;
      }

      default:
        console.error('Unknown command:', command);
        console.error('Available commands: send, send-due, list-scheduled, test, list-signatures, show-signature, interactive, draft, draft-create, draft-send, send-draft, list-drafts, show-draft, delete-draft, reply, reply-all, send-status');
        console.error('\nUsage:');
        console.error('  send                    --to <email> --subject <text> --body <text> [--signature <name>] [--html] [--attach <file>]');
        console.error('  send                    --to <email> --subject <text> --body-file <file> [--signature <name>] [--html-file <file>] [--attach <file>]');
        console.error('  send                    --to <email> --subject <text> --body <text> --send-at "YYYY-MM-DD HH:mm"');
        console.error('  send-due                Send all pending scheduled emails that are due');
        console.error('  list-scheduled          List scheduled email jobs');
        console.error('  test                    Test SMTP connection');
        console.error('  list-signatures         列出所有可用签名模板');
        console.error('  show-signature <name>   显示指定签名的详细内容');
        console.error('  interactive             Interactive mode - guided email sending wizard');
        console.error('\nDraft commands:');
        console.error('  draft                   Save email as draft (default: requires approval)');
        console.error('  draft-create            Alias for draft (backward compatibility)');
        console.error('  draft-send <id>         Alias for send-draft (backward compatibility)');
        console.error('  list-drafts             List all drafts');
        console.error('  show-draft <id>         Show draft details');
        console.error('  send-draft <id>         Send draft (requires --confirm-send)');
        console.error('  delete-draft <id>       Delete draft');
        console.error('\nReply commands:');
        console.error('  reply --message-id <UID>  Reply to email (auto "Reply All")');
        console.error('  reply-all --message-id <UID>  Reply all to email');
        console.error('\nDraft options:');
        console.error('  --to <email>            Recipient email');
        console.error('  --subject <text>        Email subject');
        console.error('  --body <text>           Email body');
        console.error('  --body-file <file>      Load body from file');
        console.error('  --attach <file>         Attach file(s)');
        console.error('  --signature <name>      Use signature template');
        console.error('  --language <lang>       Draft language (en/cn)');
        console.error('  --intent <type>         Draft intent (inquiry/reply/followup)');
        console.error('  --no-approval           Skip approval requirement');
        console.error('  --confirm-send          Confirm sending (required for send-draft)');
        console.error('  --dry-run               Preview without sending');
        console.error('  --json                  Output as JSON');
        console.error('\nStatus commands:');
        console.error('  send-status [id] [field]  Check delivery status (default: recent 10)');
        console.error('  status [id] [field]       Alias for send-status');
        console.error('\nStatus examples:');
        console.error('  node smtp.js send-status                          - Show recent 10 statuses');
        console.error('  node smtp.js send-status 5 index                  - Show 5th email status');
        console.error('  node smtp.js send-status "customer@example.com" to - Show status by recipient');
        console.error('  node smtp.js send-status "Product Inquiry" subject - Show status by subject');
        process.exit(1);
    }

    console.log(JSON.stringify(result, null, 2));
  } catch (err) {
    console.error('Error:', err.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = {
  parseSendAt,
  prepareSendOptions,
  sendEmail,
  scheduleEmail,
  sendDueScheduledEmails,
  listScheduledEmails,
  processScheduledFile,
  SCHEDULED_DIR,
};
