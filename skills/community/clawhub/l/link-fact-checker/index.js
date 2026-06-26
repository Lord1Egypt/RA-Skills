/**
 * Link & Fact Checker Skill for OpenClaw
 * Check if a URL is accessible and verify news facts
 */

async function checkUrlAccessibility(url) {
  const response = await fetch(url, { method: 'HEAD', timeout: 5000 });
  return {
    accessible: response.ok,
    status: response.status
  };
}

async function getPageTitle(url) {
  try {
    const resp = await fetch(url);
    const html = await resp.text();
    const titleMatch = html.match(/<title>(.*?)<\/title>/i);
    return titleMatch ? titleMatch[1].trim() : null;
  } catch (e) {
    return null;
  }
}

module.exports = {
  name: 'link-fact-checker',
  description: 'Check URL accessibility and verify news facts',
  
  async run(args) {
    const { url, fact } = args;
    
    // Check URL accessibility
    let checkResult = null;
    if (url) {
      try {
        const result = await checkUrlAccessibility(url);
        const title = await getPageTitle(url);
        checkResult = {
          url,
          accessible: result.accessible,
          statusCode: result.status,
          title
        };
      } catch (e) {
        checkResult = {
          url,
          accessible: false,
          error: e.message
        };
      }
    }
    
    return {
      checkedUrl: checkResult,
      checkedFact: fact ? "Pending cross-verification" : null
    };
  }
};
