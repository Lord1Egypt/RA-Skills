# KYC Vault — OpenClaw Skill

**English** | [中文](#中文说明)

Automate KYC identity verification on any website. Store your documents locally, get asked for permission before every upload, and let the AI handle the rest.

---

## How It Works

1. You put your identity documents in a local folder on your computer
2. You give OpenClaw a website URL
3. The Skill navigates to the KYC page, identifies what's needed, and asks your permission before touching any file
4. It uploads your documents and fills in the form automatically

Your files never leave your computer through any server — everything goes directly from your machine to the target website via your browser.

---

## Installation

### Step 1 — Install OpenClaw

Download and set up OpenClaw from [openclaw.ai](https://openclaw.ai).

### Step 2 — Install This Skill

```bash
clawhub install kyc-vault
```

### Step 3 — Create Your Identity Vault

```bash
mkdir -p ~/identity-vault
curl -o ~/identity-vault/manifest.json \
  https://raw.githubusercontent.com/seamao/kyc-vault-skill-/main/manifest.template.json
```

### Step 4 — Fill In Your Details

Open `~/identity-vault/manifest.json` in any text editor and replace the placeholder values with your real information (name, date of birth, nationality, etc.).

### Step 5 — Add Your Documents

Place your identity photos and files into `~/identity-vault/`. Make sure the filenames match what you wrote in `manifest.json`:

```
~/identity-vault/
  ├── manifest.json
  ├── palau_id_holding.jpg    ← Photo of you holding your Palau ID
  ├── passport_front.jpg      ← Passport photo page
  ├── selfie.jpg              ← Face photo
  └── address_proof.pdf       ← Proof of address
```

### Step 6 — Activate the Skill

In OpenClaw chat, send:

```
/skills refresh
```

---

## Usage

| Command | What it does |
|---------|-------------|
| `kyc https://example.com` | Start KYC on a website |
| `kyc list` | View your available documents |
| `kyc setup` | Guided vault setup walkthrough |
| `kyc status https://example.com` | Check your verification status |

**Example:**

> You: `kyc https://binance.com`
>
> KYC Vault: `🔍 Domain confirmation — You are about to interact with: binance.com. Is this correct?`
>
> You: `yes`
>
> KYC Vault: `⚠️ Authorization request — File: palau_id_holding.jpg · Type: Palau ID with selfie · Upload to: binance.com. Allow?`
>
> You: `yes`
>
> *(uploads file, fills form, asks before submitting)*

---

## Security

- **All files stay on your machine.** No server is involved. Uploads go directly from your browser to the target site.
- **Every file requires individual permission.** There is no "allow all" option — each document needs a separate confirmation.
- **Domain verification before every session.** The Skill shows you the exact domain and asks you to confirm before doing anything.
- **Prompt injection protection.** If a malicious website tries to embed instructions to bypass permissions, the Skill is designed to ignore them and warn you.

---

## Supported Document Types

| Type | Description |
|------|-------------|
| `palau_id_with_selfie` | Holding Palau Digital Residency ID |
| `palau_id` | Palau Digital Residency ID |
| `passport` | International passport |
| `government_id_with_selfie` | Holding government-issued ID |
| `government_id` | Government-issued ID |
| `selfie` | Face photo |
| `address_proof` | Utility bill or bank statement |

---

---

# 中文说明

自动完成各网站的 KYC 身份认证。证件存在本地，每次上传前都要你授权，剩下的交给 AI。

---

## 工作原理

1. 你把证件文件放在本地电脑的一个文件夹里
2. 你给 OpenClaw 一个网站链接
3. Skill 自动打开网站、找到 KYC 页面，在访问每个文件之前都会请求你的授权
4. 自动上传文件、填写表单

你的文件不经过任何服务器——所有上传都直接从你的浏览器发送到目标网站。

---

## 安装步骤

### 第一步 — 安装 OpenClaw

从 [openclaw.ai](https://openclaw.ai) 下载并完成初始设置。

### 第二步 — 安装本 Skill

```bash
clawhub install kyc-vault
```

### 第三步 — 创建你的证件库

```bash
mkdir -p ~/identity-vault
curl -o ~/identity-vault/manifest.json \
  https://raw.githubusercontent.com/seamao/kyc-vault-skill-/main/manifest.template.json
```

### 第四步 — 填写你的信息

用文本编辑器打开 `~/identity-vault/manifest.json`，把占位符替换成你的真实信息（姓名、生日、国籍等）。

### 第五步 — 放入证件文件

把证件照片放到 `~/identity-vault/`，文件名要和 `manifest.json` 里的 `filename` 字段一致：

```
~/identity-vault/
  ├── manifest.json
  ├── palau_id_holding.jpg    ← 手持帕劳ID的照片
  ├── passport_front.jpg      ← 护照照片页
  ├── selfie.jpg              ← 本人正面照
  └── address_proof.pdf       ← 地址证明文件
```

### 第六步 — 激活 Skill

在 OpenClaw 聊天里发送：

```
/skills refresh
```

---

## 使用方法

| 命令 | 说明 |
|------|------|
| `kyc https://xxx.com` | 开始对该网站做 KYC |
| `kyc list` | 查看我的证件列表 |
| `kyc setup` | 引导创建证件库 |
| `kyc status https://xxx.com` | 查看认证状态 |

**使用示例：**

> 你：`kyc https://binance.com`
>
> KYC Vault：`🔍 域名确认 — 即将访问：binance.com，这是你要完成 KYC 的网站吗？`
>
> 你：`是`
>
> KYC Vault：`⚠️ 授权请求 — 文件：palau_id_holding.jpg · 类型：手持帕劳ID · 上传到：binance.com，是否授权？`
>
> 你：`是`
>
> *（上传文件，填写表单，提交前再次确认）*

---

## 安全说明

- **文件全程留在你的电脑上。** 不经过任何服务器，直接从浏览器上传到目标网站。
- **每个文件单独授权。** 没有「全部允许」选项，每份证件都需要独立确认。
- **每次操作前验证域名。** Skill 会显示精确域名，让你确认后再开始任何操作。
- **防范提示词注入攻击。** 如果恶意网站在页面中嵌入指令试图绕过授权，Skill 会忽略并向你发出警告。

---

## 支持的证件类型

| 类型标识 | 说明 |
|---------|------|
| `palau_id_with_selfie` | 手持帕劳数字居民ID |
| `palau_id` | 帕劳数字居民ID |
| `passport` | 国际护照 |
| `government_id_with_selfie` | 手持政府颁发ID |
| `government_id` | 政府颁发ID |
| `selfie` | 本人正面照 |
| `address_proof` | 地址证明文件 |
