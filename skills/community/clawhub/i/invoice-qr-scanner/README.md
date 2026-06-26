# Invoice QR Scanner Skill

## Description

自动扫描发票收据中的二维码并填写电子发票申请的开票助手。

## Features

- ✅ **QR码识别**：使用Node.js + qrcode-reader库自动识别图片中的二维码
- ✅ **智能填充**：利用系统自动完成功能提高准确性
- ✅ **内存集成**：自动从MEMORY.md读取公司和联系信息
- ✅ **完整流程**：从识别到提交的完整开票流程
- ✅ **错误处理**：清晰的异常处理和备选方案

## Installation

克隆GitHub仓库即可使用：

```bash
git clone https://github.com/chenzhuowen/invoice-qr-scanner.git
cd invoice-qr-scanner
```

## Requirements

### System Requirements
- OpenClaw环境
- Node.js v14+
- 浏览器自动化工具

### NPM Dependencies

```bash
npm install qrcode-reader canvas
```

或者使用skill中的package.json：
```bash
cd invoice-qr-scanner/scripts
npm install
```

## Usage

### 1. 扫描二维码

```bash
node scan-qr.js <path-to-receipt-image>
```

**示例：**
```bash
node scan-qr.js /path/to/receipt.jpg
```

**输出：**
```
✅ 识别成功: https://fpkj.vpiaotong.com/tp/scan/index/...
```

### 2. 使用Skill

当用户要求扫描发票二维码时，OpenClaw会自动加载这个skill并执行以下操作：

1. 识别图片中的QR码
2. 打开开票系统URL
3. 从MEMORY.md读取公司信息
4. 填写开票申请表单
5. 确认并提交

## Configuration

### Memory Integration

此skill依赖于以下MEMORY.md中的信息：

**公司信息：**
- Company name（公司名称）
- Tax ID（税号）
- Address（地址）
- Phone number（电话）
- Bank name（开户行）
- Bank account number（银行账号）

**联系信息：**
- Mobile phone numbers（手机号）
- Email addresses（邮箱）

当填写表单时，skill会自动从MEMORY.md读取这些信息。

## Workflow

```
┌─────────────┐
│ 1. QR识别  │ → 使用qrcode-reader扫描图片
└─────────────┘
       ↓
┌─────────────┐
│ 2. 进入系统  │ → 浏览器打开URL
└─────────────┘
       ↓
┌─────────────┐
│ 3. 信息检索  │ → 从MEMORY.md读取
└─────────────┘
       ↓
┌─────────────┐
│ 4. 填写表单  │ → 自动填充+利用自动完成
└─────────────┘
       ↓
┌─────────────┐
│ 5. 确认提交  │ → 核对并提交
└─────────────┘
```

## File Structure

```
invoice-qr-scanner/
├── SKILL.md          # OpenClaw技能定义文件
└── scripts/
    ├── scan-qr.js     # QR码识别脚本
    └── package.json    # NPM依赖配置
```

## Examples

### 示例1：基本开票流程

**用户：** "帮我扫一下这张发票收据的二维码并开发票"

**技能执行：**
1. 识别图片中的QR码
2. 提取开票URL
3. 自动打开URL
4. 从MEMORY读取公司信息
5. 填写表单
6. 提交开票

### 示例2：识别失败处理

**用户：** "这张图片扫不出来"

**技能执行：**
1. 尝试识别
2. 识别失败
3. 询问用户："请提供开票URL或重新拍照"

## Troubleshooting

### QR码识别失败

**问题：** 扫描脚本无法识别二维码

**解决方案：**
1. 确保图片清晰，二维码完整可见
2. 检查图片格式（支持JPEG、PNG等）
3. 手动提供开票URL
4. 使用手机扫描并提供URL

### 依赖安装失败

**问题：** npm install canvas失败

**原因：** canvas需要系统依赖（libcairo、libpango等）

**解决方案：**
1. 跳过canvas安装（已全局安装或有其他方式）
2. 或者安装系统依赖：
   ```bash
   sudo apt-get install libcairo2-dev libpango1.0-dev
   ```

## Tested Platforms

- ✅ Node.js v22.22.0
- ✅ Linux (Ubuntu)
- ✅ qrcode-reader库
- ✅ 实际发票收据测试通过

## License

MIT License

## Author

Created for OpenClaw - 2026-03-03

## Support

For issues or questions, please refer to OpenClaw documentation at:
https://docs.openclaw.ai

## Repository

GitHub Repository: https://github.com/chenzhuowen/invoice-qr-scanner
