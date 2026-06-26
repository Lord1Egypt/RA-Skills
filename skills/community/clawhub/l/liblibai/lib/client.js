const { LiblibAI } = require('liblibai');

class LiblibAIClient {
  constructor(options = {}) {
    this.accessKey = options.accessKey || process.env.LIBLIBAI_ACCESS_KEY;
    this.secretKey = options.secretKey || process.env.LIBLIBAI_SECRET_KEY;
    this.baseURL = options.baseURL || process.env.LIBLIBAI_BASE_URL || 'https://openapi.liblibai.cloud';

    if (!this.accessKey || !this.secretKey) {
      throw new Error('LiblibAI credentials not found. Set LIBLIBAI_ACCESS_KEY and LIBLIBAI_SECRET_KEY environment variables or pass them as options.');
    }

    this.client = new LiblibAI({
      apiKey: this.accessKey,
      apiSecret: this.secretKey,
      baseURL: this.baseURL,
    });
  }

  async text2img(params) {
    return this.client.text2img(params);
  }

  async text2imgUltra(params) {
    return this.client.text2imgUltra(params);
  }

  async img2img(params) {
    return this.client.img2img(params);
  }

  async img2imgUltra(params) {
    return this.client.img2imgUltra(params);
  }

  async runComfy(params) {
    return this.client.runComfy(params);
  }

  async uploadFile(fileBuffer, filename = null) {
    return this.client.uploadFile(fileBuffer, filename);
  }

  async submitText2Img(params) {
    return this.client.submitText2Img(params);
  }

  async getStatus(generateUuid) {
    return this.client.getStatus(generateUuid);
  }

  async waitResult(generateUuid, pollingInterval = 3000, timeout = 300000) {
    return this.client.waitResult(generateUuid, pollingInterval, timeout);
  }

  async getComfyStatus(generateUuid) {
    return this.client.getComfyStatus(generateUuid);
  }

  async waitAppResult(generateUuid, pollingInterval = 3000, timeout = 300000) {
    return this.client.waitAppResult(generateUuid, pollingInterval, timeout);
  }
}

module.exports = { LiblibAIClient };
