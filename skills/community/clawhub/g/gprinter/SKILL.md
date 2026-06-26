# GP-C200V Printer Skill

佳博 (Gainscha) GP-C200V ESC/POS 热敏打印机开发技能包。

## 文件结构

```
skill/
├── CLAUDE.md              # 技能主文档 — 架构、规则、命令速查
├── esc-pos-protocol.md    # ESC/POS 协议完整参考
├── print-helper.js        # Node.js 可复用打印库
├── print-standalone.js    # 命令行打印工具
└── README.md              # 本文件
```

## 快速使用

### 1. 使用 Node.js 库打印

```javascript
const GPPrinter = require('./print-helper');

const printer = new GPPrinter({
  host: '192.168.50.189',
  port: 9100,
});

await printer.connect();

// 打印文本
const cmd = printer.buildTextCommand('Hello 世界', {
  align: 'center',
  size: 'double',
  cut: true,
});
await printer.sendRaw(cmd);

await printer.disconnect();
```

### 2. 命令行打印

```bash
# 打印文本
node print-standalone.js --text "Hello World 中文测试"

# 打印文件
node print-standalone.js --file receipt.txt

# 打印二维码
node print-standalone.js --qr "https://example.com"

# 打印条形码
node print-standalone.js --barcode CODE128 "TEST-001"

# 打印后切纸
node print-standalone.js --text "Hello" --cut

# 指定打印机
node print-standalone.js --host 192.168.1.100 --text "Test"
```

### 3. 浏览器测试页

> 可选，仅在需要浏览器打印时使用。需要启动 `h5-usb-serial/` 项目中的 `server.js` 作为 TCP 桥接。打开 `http://localhost:3000/gp-c200v.html`。

## 核心规则

1. **中文必须用 GBK 编码** — `encodeToGb2312` 映射表不完整
2. **切纸前必须走纸** — `ESC J 0xFF` + `ESC i`
3. **使用原始字节数组** — 不要用 `gpESC.createNew().setText()`

## 关键参数

| 参数 | 值 | 说明 |
|------|------|------|
| 打印机 IP | 192.168.50.189 | WiFi 地址 |
| 端口 | 9100 | RAW 打印端口 |
| 打印宽度 | 384px | 80mm 纸满宽 |
| 每行字符 | 42(标准) / 21(双倍) | 字符容量 |
