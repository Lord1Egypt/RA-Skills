#!/usr/bin/env node
/**
 * Standalone Print Script for GP-C200V
 *
 * Usage:
 *   node print-standalone.js --host 192.168.50.189 --text "Hello World"
 *   node print-standalone.js --host 192.168.50.189 --file receipt.txt
 *   node print-standalone.js --host 192.168.50.189 --qr "https://example.com"
 *   node print-standalone.js --host 192.168.50.189 --barcode CODE128 "TEST-001"
 *   node print-standalone.js --host 192.168.50.189 --cut
 */

const net = require('net');

// --- Argument Parsing ---
function parseArgs(argv) {
  const args = {
    host: '192.168.50.189',
    port: 9100,
    text: '',
    file: '',
    qr: '',
    barcodeType: 'CODE128',
    barcodeData: '',
    image: '',
    align: 'left',
    size: 'normal',
    cut: false,
    feed: true,
    feedDots: 0xFF,
  };

  for (let i = 2; i < argv.length; i++) {
    switch (argv[i]) {
      case '--host': args.host = argv[++i]; break;
      case '--port': args.port = parseInt(argv[++i]); break;
      case '--text': args.text = argv[++i]; break;
      case '--file': args.file = argv[++i]; break;
      case '--qr': args.qr = argv[++i]; break;
      case '--barcode': args.barcodeType = argv[++i]; args.barcodeData = argv[++i]; break;
      case '--image': args.image = argv[++i]; break;
      case '--align': args.align = argv[++i]; break;
      case '--size': args.size = argv[++i]; break;
      case '--cut': args.cut = true; break;
      case '--no-feed': args.feed = false; break;
      case '--help':
      case '-h':
        console.log(`
Usage: node print-standalone.js [options]

Options:
  --host <ip>        Printer IP (default: 192.168.50.189)
  --port <port>      Printer port (default: 9100)
  --text <string>    Print text
  --file <path>      Print text from file
  --qr <string>      Print QR code
  --barcode <type> <data>  Print barcode (CODE128, CODE39, EAN13, etc.)
  --image <path>     Print image (PNG/JPG)
  --align <left|center|right>  Text alignment
  --size <normal|double|width|height>  Character size
  --cut              Cut paper after printing
  --no-feed          Don't feed paper before cut
  --help             Show this help
        `.trim());
        process.exit(0);
    }
  }

  return args;
}

// --- GBK Encoding ---
const iconv = require('iconv-lite');

function encodeGBK(text) {
  return Array.from(iconv.encode(text, 'gbk'));
}

// --- Command Builders ---
function buildTextCommand(text, options) {
  const cmd = [];
  cmd.push(0x1B, 0x40); // Init

  const alignMap = { left: 0, center: 1, right: 2 };
  cmd.push(0x1B, 0x61, alignMap[options.align || 'left']);

  const sizeMap = { normal: 0x00, double: 0x11, width: 0x01, height: 0x10 };
  cmd.push(0x1B, 0x21, sizeMap[options.size || 'normal']);

  for (const line of text.split('\n')) {
    cmd.push(...encodeGBK(line));
    cmd.push(0x0A);
  }

  if (options.cut) {
    cmd.push(0x1B, 0x4A, options.feed ? 0xFF : 0x00);
    cmd.push(0x1B, 0x69);
  }

  return cmd;
}

function buildQRCommand(content, options) {
  const cmd = [];
  cmd.push(0x1B, 0x40);
  cmd.push(0x1B, 0x61, 1); // Center

  const dataBytes = encodeGBK(content);
  const len = dataBytes.length + 3;

  // Error correction M
  cmd.push(0x1D, 0x28, 0x6B, 0x03, 0x00, 0x31, 0x45, 49);
  // Module size 6
  cmd.push(0x1D, 0x28, 0x6B, 0x03, 0x00, 0x31, 0x43, 6);
  // Data
  cmd.push(0x1D, 0x28, 0x6B, len & 0xFF, (len >> 8) & 0xFF, 0x31, 0x50, 0x30);
  cmd.push(...dataBytes);
  // Print
  cmd.push(0x1D, 0x28, 0x6B, 0x03, 0x00, 0x31, 0x51, 0x30);
  cmd.push(0x0A);

  if (options.cut) {
    cmd.push(0x1B, 0x4A, 0xFF);
    cmd.push(0x1B, 0x69);
  }

  return cmd;
}

function buildBarcodeCommand(type, data, options) {
  const cmd = [];
  cmd.push(0x1B, 0x40);
  cmd.push(0x1B, 0x61, 1); // Center

  const typeMap = {
    'UPC-A': 0x41, 'UPC-E': 0x42, 'EAN13': 0x43, 'EAN8': 0x44,
    'CODE39': 0x45, 'ITF': 0x46, 'CODABAR': 0x47,
    'CODE93': 0x48, 'CODE128': 0x49,
  };

  cmd.push(0x1D, 0x68, 80);   // Height
  cmd.push(0x1D, 0x77, 3);    // Width
  cmd.push(0x1D, 0x6B, typeMap[type] || 0x49, data.length);
  for (const c of data) cmd.push(c.charCodeAt(0));
  cmd.push(0x0A);

  if (options.cut) {
    cmd.push(0x1B, 0x4A, 0xFF);
    cmd.push(0x1B, 0x69);
  }

  return cmd;
}

// --- Send ---
async function sendToPrinter(host, port, cmd) {
  return new Promise((resolve, reject) => {
    const socket = new net.Socket();
    socket.setTimeout(10000);
    socket.setKeepAlive(true, 1000);
    socket.setNoDelay(true);

    socket.on('connect', () => {
      console.log(`Connected to ${host}:${port}`);
      socket.write(Buffer.from(cmd), (err) => {
        if (err) {
          console.error('Send error:', err.message);
          socket.destroy();
          reject(err);
        } else {
          console.log(`Sent ${cmd.length} bytes`);
          socket.end();
          socket.on('close', () => resolve());
        }
      });
    });

    socket.on('error', (err) => {
      reject(err);
    });

    socket.on('timeout', () => {
      console.error('Connection timeout');
      socket.destroy();
      reject(new Error('Timeout'));
    });

    console.log(`Connecting to ${host}:${port}...`);
    socket.connect(port, host);
  });
}

// --- Main ---
async function main() {
  const args = parseArgs(process.argv);

  let cmd = [];

  if (args.file) {
    const fs = require('fs');
    args.text = fs.readFileSync(args.file, 'utf-8');
  }

  if (args.text) {
    cmd = buildTextCommand(args.text, {
      align: args.align,
      size: args.size,
      cut: args.cut,
      feed: args.feed,
    });
  }

  if (args.qr) {
    cmd = buildQRCommand(args.qr, { cut: args.cut });
  }

  if (args.barcodeData) {
    cmd = buildBarcodeCommand(args.barcodeType, args.barcodeData, { cut: args.cut });
  }

  if (args.image) {
    console.error('Image printing requires a browser context. Use gp-c200v.html instead.');
    process.exit(1);
  }

  if (cmd.length === 0) {
    console.error('Nothing to print. Use --text, --file, --qr, or --barcode.');
    process.exit(1);
  }

  try {
    await sendToPrinter(args.host, args.port, cmd);
    console.log('Print successful');
  } catch (err) {
    console.error('Print failed:', err.message);
    process.exit(1);
  }
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
