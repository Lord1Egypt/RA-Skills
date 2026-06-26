// HelloFresh Skill - Kernel Browser Integration
// Uses Kernel.sh cloud browsers for cloud deployment

import { Kernel, Browser, Page } from '@onkernel/sdk';
import { chromium } from 'playwright';

let kernel: Kernel | null = null;
let kernelBrowser: Browser | null = null;
let kernelSessionId: string | null = null;
let initPromise: Promise<Browser> | null = null;

const KERNEL_API_KEY = process.env.KERNEL_API_KEY;
const USE_KERNEL = process.env.USE_KERNEL === 'true';

// Initialize Kernel browser (with mutex to prevent race conditions)
export async function initKernelBrowser(): Promise<Browser> {
  // If already initialized, return existing browser
  if (kernelBrowser) {
    return kernelBrowser;
  }
  
  // If init in progress, wait for it
  if (initPromise) {
    return initPromise;
  }
  
  // Start initialization
  initPromise = doInitKernelBrowser();
  
  try {
    kernelBrowser = await initPromise;
    return kernelBrowser;
  } finally {
    initPromise = null;
  }
}

async function doInitKernelBrowser(): Promise<Browser> {
  if (!KERNEL_API_KEY) {
    throw new Error('KERNEL_API_KEY not set. Set USE_KERNEL=false for local mode.');
  }
  
  console.log('Creating Kernel browser...');
  kernel = new Kernel({ apiKey: KERNEL_API_KEY });
  
  let kb;
  try {
    kb = await kernel.browsers.create();
    kernelSessionId = kb.session_id;
    console.log('Kernel session:', kernelSessionId);
  } catch (createError) {
    kernel = null;
    throw createError;
  }
  
  let browser;
  try {
    browser = await chromium.connectOverCDP(kb.cdp_ws_url);
  } catch (connectError) {
    try {
      await kernel.browsers.deleteByID(kernelSessionId);
    } catch (deleteError) {
      console.error('Failed to delete Kernel session:', deleteError);
    }
    kernelSessionId = null;
    throw connectError;
  }
  
  console.log('Connected to Kernel browser');
  return browser;
}

// Close Kernel browser
export async function closeKernelBrowser(): Promise<void> {
  if (kernelBrowser) {
    try {
      await kernelBrowser.close();
    } catch (e) {
      console.error('Error closing browser:', e);
    }
    kernelBrowser = null;
  }
  
  if (kernel && kernelSessionId) {
    try {
      await kernel.browsers.deleteByID(kernelSessionId);
    } catch (e) {
      console.error('Error deleting Kernel session:', e);
    }
    kernelSessionId = null;
    kernel = null;
  }
}

// Get the current page from Kernel browser (async)
export async function getKernelPage(): Promise<Page> {
  const browser = await initKernelBrowser();
  
  // Try to get existing page
  const existingContext = browser.contexts()[0];
  if (existingContext) {
    const existingPage = existingContext.pages()[0];
    if (existingPage) {
      return existingPage;
    }
  }
  
  // Create new page in existing context or new context
  const context = existingContext || await browser.newContext();
  return await context.newPage();
}

// Navigate to URL using Kernel (async)
export async function kernelNavigate(url: string): Promise<void> {
  const page = await getKernelPage();
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
}

// Get snapshot from Kernel (async)
export async function kernelSnapshot(): Promise<string> {
  const page = await getKernelPage();
  return await page.content();
}

// Click element in Kernel (async)
export async function kernelClick(selector: string): Promise<void> {
  const page = await getKernelPage();
  await page.click(selector);
}

// Check if using Kernel mode
export function isUsingKernel(): boolean {
  return USE_KERNEL;
}

// Export browser status
export function getKernelStatus(): { active: boolean; sessionId: string | null } {
  return {
    active: kernelBrowser !== null,
    sessionId: kernelSessionId
  };
}

// Cleanup on process exit
async function cleanup(): Promise<void> {
  console.log('Cleaning up Kernel browser...');
  await closeKernelBrowser();
}

// Register cleanup hooks
process.on('exit', () => {
  if (kernel && kernelSessionId) {
    console.log('Warning: Kernel session not cleaned up on exit');
  }
});

process.on('SIGINT', async () => {
  await cleanup();
  process.exit(0);
});

process.on('SIGTERM', async () => {
  await cleanup();
  process.exit(0);
});
