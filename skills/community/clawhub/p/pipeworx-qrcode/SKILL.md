# QR Code

Generate and decode QR codes. Two tools, zero configuration.

`create_qr` encodes any text or URL into a QR code image URL (10px to 1000px). `read_qr` decodes a QR code from any publicly accessible image URL.

## Quick start

Generate a QR code for a URL:

```bash
curl -X POST https://gateway.pipeworx.io/qrcode/mcp \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"create_qr","arguments":{"data":"https://example.com","size":300}}}'
```

The response contains a `url` field you can embed directly in `<img>` tags or download.

## Decoding

Pass any image URL containing a QR code to `read_qr` and get the decoded text back. Works with PNGs, JPEGs, and most common image formats.

```json
{
  "mcpServers": {
    "qrcode": {
      "url": "https://gateway.pipeworx.io/qrcode/mcp"
    }
  }
}
```
