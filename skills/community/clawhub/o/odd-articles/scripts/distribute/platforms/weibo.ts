/**
 * Weibo (微博) publisher via Chrome CDP.
 * Opens weibo.com/compose, fills in post content.
 */

import {
  launchChrome, getPageSession, clickElement, typeText, evaluate,
  waitForSelector, sleep, randomDelay,
  type Manifest, type PublishResult, type ChromeSession,
} from '../cdp-utils.ts';

const WEIBO_URL = 'https://weibo.com';
const FALLBACK_CDP_PORT = 9222;

const SELECTORS = {
  composeArea: '[contenteditable="true"], textarea.W_input, div.W_editor, div[node-type="text"], div.placeholder',
  publishBtn: 'a[node-type="publish"], button:has-text("发布"), div[node-type="publish"], a.W_btn_a[node-type="publish"]',
  loginIndicator: 'a[href*="setting"], div[class*="user-card"], img[class*="avatar"], div[class*="user-name"]',
  titleInput: 'input[name="title"], input[placeholder*="标题"]',
  navCompose: 'a[href*="compose"], a[href*="/publish"], div:has-text("发布微博")',
  weiboHome: 'div[node-type="feed_list"], div[class*="Feed"]',
  sendBtn: 'a.W_btn_a[node-type="submit"], a[node-type="submit"]',
};

export async function publishToWeibo(manifest: Manifest, preview: boolean): Promise<PublishResult> {
  const weiboData = manifest.outputs.weibo;
  if (!weiboData) {
    return { platform: 'weibo', status: 'skipped', message: 'No Weibo content in manifest' };
  }

  let launchResult;
  try {
    launchResult = await launchChrome(WEIBO_URL, 'weibo');
  } catch (err) {
    const errMsg = err instanceof Error ? err.message : String(err);
    console.error(`  [weibo] Launch error: ${errMsg}`);
    return {
      platform: 'weibo',
      status: 'manual',
      message: `Chrome launch failed: ${errMsg}\n\nCopy your Weibo post manually:\n${weiboData.copy.body.substring(0, 100)}...`,
    };
  }

  const { cdp, chrome } = launchResult;

  try {
    await sleep(4000);

    let session: ChromeSession;
    try {
      session = await getPageSession(cdp, 'weibo.com');
    } catch {
      return {
        platform: 'weibo',
        status: 'assisted',
        message: 'Page opened. Please log in to Weibo, then retry.',
      };
    }

    // Check if logged in - look for user avatar or settings
    const isLoggedIn = await evaluate<boolean>(session, `
      !!(
        document.querySelector('a[href*="setting"]') ||
        document.querySelector('div[class*="user-card"]') ||
        document.querySelector('img[class*="avatar"]')
      )
    `);
    
    if (!isLoggedIn) {
      const currentUrl = await evaluate<string>(session, 'window.location.href');
      if (currentUrl.includes('login') || currentUrl.includes('passport')) {
        return {
          platform: 'weibo',
          status: 'assisted',
          message: 'Login required. Please log in to Weibo, then run /distribute again.',
        };
      }
    }

    // Try to find and click compose button on the home page
    const composeBtnSelectors = [
      'a[href*="/compose"]',
      'a[href*="compose"]', 
      'div[node-type="publish"]',
      'a[node-type="publish"]',
      'div:has-text("发布微博")',
      'a:has-text("发微博")',
      'span:has-text("发微博")'
    ];
    
    console.log('  Looking for compose button...');
    for (const sel of composeBtnSelectors) {
      const hasBtn = await evaluate<boolean>(session, `!!document.querySelector('${sel.replace(/'/g, "\\'")}')`);
      if (hasBtn) {
        console.log(`  Found: ${sel}, clicking...`);
        await clickElement(session, sel);
        await sleep(3000);
        break;
      }
    }
    
    // Debug: get all textareas and editable elements
    const inputs = await evaluate<any[]>(session, `
      Array.from(document.querySelectorAll('textarea, [contenteditable="true"], input')).map(el => ({
        tag: el.tagName,
        id: el.id,
        class: el.className?.substring(0, 50),
        placeholder: el.getAttribute('placeholder')?.substring(0, 30)
      }))
    `);
    console.log(`  Found ${inputs.length} input elements:`, inputs.slice(0, 5));
    
    // Try to find compose area
    const hasEditor = await waitForSelector(session, SELECTORS.composeArea, 10_000);
    if (hasEditor) {
      await clickElement(session, SELECTORS.composeArea);
      await randomDelay();
      
      // Build content: title (if any) + body + tags
      const fullContent = weiboData.copy.body + '\n\n' + weiboData.copy.tags.map(t => '#' + t).join(' ');
      await typeText(session, fullContent);
      console.log(`  Content filled (${fullContent.length} chars)`);
    } else {
      // Try alternative: look for any textarea or editable area
      const hasTextArea = await waitForSelector(session, 'textarea, [contenteditable="true"]', 5_000);
      if (hasTextArea) {
        await clickElement(session, 'textarea, [contenteditable="true"]');
        await randomDelay();
        const fullContent = weiboData.copy.body + '\n\n' + weiboData.copy.tags.map(t => '#' + t).join(' ');
        await typeText(session, fullContent);
        console.log(`  Content filled (${fullContent.length} chars)`);
      } else {
        return {
          platform: 'weibo',
          status: 'assisted',
          message: 'Editor not found. Weibo is open, please paste content manually.',
        };
      }
    }

    if (!preview) {
      await sleep(1500);
      
      // Look for publish button
      const publishSelectors = [
        'a[node-type="publish"]',
        'a.W_btn_a[node-type="publish"]',
        'button:has-text("发布")',
        'a:has-text("发布")'
      ];
      
      for (const sel of publishSelectors) {
        const hasBtn = await waitForSelector(session, sel, 2_000);
        if (hasBtn) {
          await randomDelay(500, 1000);
          await clickElement(session, sel);
          await sleep(3000);
          
          const finalUrl = await evaluate<string>(session, 'window.location.href');
          if (finalUrl.includes('weibo.com/u/') || finalUrl.includes('detail') || finalUrl.includes('status')) {
            return { platform: 'weibo', status: 'success', message: 'Published to Weibo' };
          }
          return { platform: 'weibo', status: 'success', message: 'Published to Weibo (check manually)' };
        }
      }
      
      // Try Ctrl+Enter shortcut
      await randomDelay(500, 1000);
      await session.cdp.send('Input.dispatchKeyEvent', {
        type: 'keyDown', key: 'Control', code: 'ControlLeft', modifiers: 0x4,
      }, { sessionId: session.sessionId });
      await session.cdp.send('Input.dispatchKeyEvent', {
        type: 'keyDown', key: 'Enter', code: 'Enter', windowsVirtualKeyCode: 13,
      }, { sessionId: session.sessionId });
      await sleep(2000);
      
      return { 
        platform: 'weibo', 
        status: 'assisted', 
        message: 'Content filled, please click publish manually.' 
      };
    }

    return {
      platform: 'weibo',
      status: 'assisted',
      message: `Content pre-filled. Tags: ${weiboData.copy.tags.join(', ')}`,
    };
  } catch (err) {
    return {
      platform: 'weibo',
      status: 'manual',
      message: `CDP error: ${err instanceof Error ? err.message : String(err)}`,
    };
  } finally {
    cdp.close();
  }
}