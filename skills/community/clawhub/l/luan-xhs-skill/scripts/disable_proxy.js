// Helper to disable proxy environment variables when useProxy is false
module.exports = {
  apply: function (useProxy) {
    if (useProxy === false) {
      delete process.env.HTTP_PROXY;
      delete process.env.HTTPS_PROXY;
      delete process.env.http_proxy;
      delete process.env.https_proxy;
      // also clear common npm proxy vars
      delete process.env.NPM_CONFIG_PROXY;
      delete process.env.NPM_CONFIG_HTTPS_PROXY;
      // log a short message
      try { console.log('[xiaohongshu-ops] Proxy disabled for this run (useProxy=false)'); } catch (e) {}
    }
  }
};
