# 体检预约信息

## 预约链接

```
https://www.ihaola.com.cn/launch/haola/pe?urlsrc=brief&welfareid=xxx&ruleid=xxx
```

## 二维码生成

### Node.js（推荐，容器内可用）

```javascript
const { generateQR } = require('./scripts/generate_qr.js')
await generateQR('/path/to/output.png', { welfareid: 'xxx', ruleid: 'xxx' })
```

命令行：
```bash
node scripts/generate_qr.js [output_path] [welfareid] [ruleid]
```

## 使用说明

1. 推荐完体检项目后，告知用户可以扫码预约
2. 使用 Node.js 生成二维码图片（推荐）
3. 将图片发送给用户（微信支持直接发送图片）

---

**最后更新：** 2026-03-29
