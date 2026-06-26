/**
 * GP-C200V Print Helper Library
 *
 * Reusable module for building ESC/POS commands and sending them
 * to the GP-C200V printer via the Node.js TCP bridge (server.js).
 *
 * Usage:
 *   const GPPrinter = require('./print-helper')
 *   const printer = new GPPrinter({ host: '192.168.50.189', port: 9100, serverPort: 3000 })
 *   await printer.connect()
 *   await printer.printText('Hello World')
 *   await printer.disconnect()
 */

const net = require('net');
const iconv = require('iconv-lite');

// GBK encoding — using iconv-lite for full character coverage
function encodeGBK(text) {
  return Array.from(iconv.encode(text, 'gbk'));
}

class GPPrinter {
  constructor(options = {}) {
    this.host = options.host || '192.168.50.189';
    this.port = options.port || 9100;
    this.serverPort = options.serverPort || 3000;
    this.serverHost = options.serverHost || 'localhost';
    this.connected = false;
    this.socket = null;
    this.heartbeatInterval = null;
  }

  // ====== Connection ======

  async connect() {
    return new Promise((resolve, reject) => {
      const socket = new net.Socket();
      socket.setTimeout(10000);
      socket.setKeepAlive(true, 1000);
      socket.setNoDelay(true);

      socket.on('connect', () => {
        this.socket = socket;
        this.connected = true;
        this._startHeartbeat();
        resolve(this);
      });

      socket.on('error', (err) => {
        reject(err);
      });

      socket.on('timeout', () => {
        socket.destroy();
        reject(new Error('Connection timeout'));
      });

      socket.connect(this.host, this.port);
    });
  }

  async disconnect() {
    if (this.heartbeatInterval) {
      clearInterval(this.heartbeatInterval);
      this.heartbeatInterval = null;
    }
    if (this.socket) {
      this.socket.destroy();
      this.socket = null;
    }
    this.connected = false;
  }

  // ====== Direct TCP send (bypasses HTTP bridge) ======

  async sendRaw(cmdArray) {
    if (!this.connected || !this.socket) {
      throw new Error('Printer not connected');
    }
    const buffer = Buffer.from(cmdArray);
    return new Promise((resolve, reject) => {
      this.socket.write(buffer, (err) => {
        if (err) reject(err);
        else resolve();
      });
    });
  }

  // ====== HTTP Bridge send ======

  async sendViaBridge(cmdArray) {
    const resp = await fetch(`http://${this.serverHost}:${this.serverPort}/send`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: cmdArray }),
    });
    const data = await resp.json();
    if (!data.success) throw new Error(data.error);
    return data;
  }

  // ====== Heartbeat ======

  _startHeartbeat() {
    this.heartbeatInterval = setInterval(() => {
      if (this.socket && !this.socket.destroyed) {
        this.socket.write(Buffer.from([0x00]), () => {});
      }
    }, 3000);
  }

  // ====== Build Commands ======

  /**
   * Build an ESC/POS command array for text printing
   *
   * @param {string} text - Text to print (supports Chinese via GBK)
   * @param {object} options
   * @param {'left'|'center'|'right'} options.align - Text alignment
   * @param {'normal'|'double'|'width'|'height'} options.size - Character size
   * @param {boolean} options.bold - Bold text
   * @param {boolean} options.underline - Underline text
   * @param {boolean} options.feed - Feed paper before cut
   * @param {boolean} options.cut - Cut paper after print
   * @returns {number[]} ESC/POS byte array
   */
  buildTextCommand(text, options = {}) {
    const cmd = [];

    // Init
    cmd.push(0x1B, 0x40);

    // Alignment
    const alignMap = { left: 0, center: 1, right: 2 };
    const align = alignMap[options.align || 'left'];
    cmd.push(0x1B, 0x61, align);

    // Size
    const sizeMap = {
      normal: 0x00,
      double: 0x11,
      width: 0x01,
      height: 0x10,
    };
    cmd.push(0x1B, 0x21, sizeMap[options.size || 'normal']);

    // Bold
    if (options.bold) {
      cmd.push(0x1B, 0x45, 1);
    }

    // Underline
    if (options.underline) {
      cmd.push(0x1B, 0x2D, 1);
    }

    // Lines
    const lines = text.split('\n');
    for (const line of lines) {
      cmd.push(...encodeGBK(line));
      cmd.push(0x0A); // LF
    }

    // Feed and cut
    if (options.cut) {
      cmd.push(0x1B, 0x4A, 0xFF); // Feed 255 dots
      cmd.push(0x1B, 0x69);       // Cut
    } else if (options.feed) {
      cmd.push(0x1B, 0x4A, options.feed === true ? 0xFF : options.feed);
    }

    return cmd;
  }

  /**
   * Build a barcode command
   *
   * @param {string} type - Barcode type (CODE128, CODE39, EAN13, etc.)
   * @param {string} content - Barcode data
   * @param {object} options
   * @param {number} options.height - Barcode height in dots (default 80)
   * @param {number} options.width - Barcode width multiplier (default 3)
   * @param {boolean} options.cut - Cut after printing
   * @returns {number[]}
   */
  buildBarcodeCommand(type, content, options = {}) {
    const cmd = [];
    cmd.push(0x1B, 0x40); // Init
    cmd.push(0x1B, 0x61, 1); // Center

    const typeMap = {
      'UPC-A': 0x41, 'UPC-E': 0x42, 'EAN13': 0x43, 'EAN8': 0x44,
      'CODE39': 0x45, 'ITF': 0x46, 'CODABAR': 0x47,
      'CODE93': 0x48, 'CODE128': 0x49,
    };
    const typeCode = typeMap[type] || 0x49;

    cmd.push(0x1D, 0x68, options.height || 80);   // Height
    cmd.push(0x1D, 0x77, options.width || 3);     // Width
    cmd.push(0x1D, 0x6B, typeCode, content.length); // Type + length
    for (const c of content) cmd.push(c.charCodeAt(0));
    cmd.push(0x0A);

    if (options.cut) {
      cmd.push(0x1B, 0x4A, 0xFF);
      cmd.push(0x1B, 0x69);
    }

    return cmd;
  }

  /**
   * Build a QR code command
   *
   * @param {string} content - QR code data
   * @param {object} options
   * @param {'L'|'M'|'Q'|'H'} options.ecLevel - Error correction (default 'M')
   * @param {number} options.moduleSize - Module size 1-15 (default 6)
   * @param {boolean} options.cut - Cut after printing
   * @returns {number[]}
   */
  buildQRCommand(content, options = {}) {
    const cmd = [];
    cmd.push(0x1B, 0x40); // Init
    cmd.push(0x1B, 0x61, 1); // Center

    const ecMap = { L: 48, M: 49, Q: 50, H: 51 };
    const ecLevel = ecMap[options.ecLevel || 'M'];
    const moduleSize = Math.min(15, Math.max(1, options.moduleSize || 6));

    // Error correction
    cmd.push(0x1D, 0x28, 0x6B, 0x03, 0x00, 0x31, 0x45, ecLevel);
    // Module size
    cmd.push(0x1D, 0x28, 0x6B, 0x03, 0x00, 0x31, 0x43, moduleSize);

    // Data (GBK encoded)
    const dataBytes = encodeGBK(content);
    const len = dataBytes.length + 3;
    cmd.push(0x1D, 0x28, 0x6B, len & 0xFF, (len >> 8) & 0xFF, 0x31, 0x50, 0x30);
    cmd.push(...dataBytes);

    // Print QR
    cmd.push(0x1D, 0x28, 0x6B, 0x03, 0x00, 0x31, 0x51, 0x30);
    cmd.push(0x0A);

    if (options.cut) {
      cmd.push(0x1B, 0x4A, 0xFF);
      cmd.push(0x1B, 0x69);
    }

    return cmd;
  }

  /**
   * Build a bitmap image command
   *
   * @param {object} imageData - { width, height, pixels: Uint8Array }
   * @param {object} options
   * @param {number} options.threshold - Binarization threshold (default 128)
   * @param {boolean} options.cut - Cut after printing
   * @returns {number[]}
   */
  buildImageCommand(imageData, options = {}) {
    const { width, height, pixels } = imageData;
    const threshold = options.threshold || 128;
    const bytesPerRow = Math.ceil(width / 8);

    // Convert to 1-bit bitmap (MSB first, row-major)
    const bitmapData = [];
    for (let y = 0; y < height; y++) {
      for (let byteIndex = 0; byteIndex < bytesPerRow; byteIndex++) {
        let byte = 0;
        for (let bit = 0; bit < 8; bit++) {
          const x = byteIndex * 8 + bit;
          if (x < width) {
            const gray = pixels[y * width + x];
            if (gray < threshold) byte |= (1 << (7 - bit));
          }
        }
        bitmapData.push(byte);
      }
    }

    const cmd = [];
    cmd.push(0x1B, 0x40); // Init
    cmd.push(0x1B, 0x61, 1); // Center

    // GS v 0 — raster bitmap
    cmd.push(0x1D, 0x76, 0x30, 0x00);
    cmd.push(bytesPerRow & 0xFF, (bytesPerRow >> 8) & 0xFF); // xL, xH
    cmd.push(height & 0xFF, (height >> 8) & 0xFF);           // yL, yH
    cmd.push(...bitmapData);

    if (options.cut) {
      cmd.push(0x1B, 0x4A, 0xFF);
      cmd.push(0x1B, 0x69);
    }

    return cmd;
  }

  /**
   * Build a feed + cut command
   */
  buildCutCommand(feedDots = 0xFF) {
    return [0x1B, 0x4A, feedDots, 0x1B, 0x69];
  }
}

module.exports = GPPrinter;
