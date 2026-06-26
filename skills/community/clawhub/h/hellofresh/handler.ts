// HelloFresh Skill - Core Command Handlers
// Uses OpenClaw browser tool (profile="chrome") or Kernel.sh cloud browsers

const BASE_URL = 'https://www.hellofresh.ca';
const SESSION_FILE = `${process.env.HOME}/.openclaw/hellofresh/session.json`;
const RECIPE_CACHE_FILE = `${process.env.HOME}/.openclaw/hellofresh/recipes.json`;

// ============ BROWSER MODE CONFIG ============

const USE_KERNEL = process.env.USE_KERNEL === 'true';

// Import Kernel functions if needed
let kernelBrowser: {
  initKernelBrowser: () => Promise<any>;
  kernelNavigate: (url: string) => Promise<void>;
  kernelSnapshot: () => Promise<string>;
  kernelClick: (ref: string) => Promise<void>;
  closeKernelBrowser: () => Promise<void>;
  isUsingKernel: () => boolean;
} | null = null;

async function getKernelBrowser() {
  if (!kernelBrowser) {
    const kb = await import('./kernelBrowser');
    kernelBrowser = {
      initKernelBrowser: kb.initKernelBrowser,
      kernelNavigate: kb.kernelNavigate,
      kernelSnapshot: kb.kernelSnapshot,
      kernelClick: kb.kernelClick,
      closeKernelBrowser: kb.closeKernelBrowser,
      isUsingKernel: kb.isUsingKernel
    };
  }
  return kernelBrowser;
}

// Browser abstraction layer
async function hfNavigate(url: string): Promise<void> {
  if (USE_KERNEL) {
    const kb = await getKernelBrowser();
    await kb.initKernelBrowser();
    await kb.kernelNavigate(url);
  } else {
    await browser({ action: 'navigate', profile: 'chrome', targetUrl: url });
  }
}

async function hfSnapshot(): Promise<string> {
  if (USE_KERNEL) {
    const kb = await getKernelBrowser();
    return await kb.kernelSnapshot();
  } else {
    const result = await browser({ action: 'snapshot', profile: 'chrome' });
    return result.result?.html || '';
  }
}

async function hfClick(ref: string): Promise<void> {
  if (USE_KERNEL) {
    const kb = await getKernelBrowser();
    await kb.kernelClick(`[ref="${ref}"]`);
  } else {
    await browser({ action: 'act', profile: 'chrome', request: { kind: 'click', ref } });
  }
}

async function hfClose(): Promise<void> {
  if (USE_KERNEL && kernelBrowser) {
    await kernelBrowser.closeKernelBrowser();
  }
}

// ============ CONSTANTS ============

const DEFAULT_TIMEOUT_MS = 3000;
const PAGE_LOAD_TIMEOUT_MS = 5000;

// Regex patterns (extracted for reuse)
const PATTERNS = {
  // Match delivery date: "Sun., Mar. 15" or "Mon, January 5"
  deliveryDate: /([A-Z][a-z]{1,2}\.?,\s*[A-Z][a-z]+\.?\s*\d{1,2})/i,
  
  // Match cutoff: "Edit delivery by Wed., Mar. 11"
  cutoffDate: /Edit delivery by\s+([A-Z][a-z]{1,2}\.?,\s*[A-Z][a-z]+\.?\s*\d{1,2})/i,
  
  // Match recipe: heading + time + calories + protein
  recipe: /heading\s+"([^"]+)"[^}]+?(\d+)\s*min[^}]+?(\d+)\s*Cal[^}]+?(\d+)g/i,
  
  // Match past delivery: "Delivered on Sun., Feb. 22"
  pastDelivery: /Delivered on\s+([A-Z][a-z]{2,}\.?\,?\s*[A-Z][a-z]{2,}\.?\,?\s*\d{1,2})/gi,
  
  // Match tags
  recipeTag: /listitem\s+"([^"]+)"[^}]+?heading\s+"([^"]+)"/gi
};

// ============ TYPES ============

export interface Session {
  setupComplete: boolean;
  subscription?: Subscription;
  preferences: UserPreferences;
  notifications: NotificationSettings;
}

interface Subscription {
  id: string;
  region: string;
  planName: string;
  mealsPerBox: number;
  deliveryDay: string;
  deliveryWindow: string;
  pricePerBox: number;
  pricePerServing: number;
  shipping: number;
  deliveryAddress: string;
  paymentMethod: string;
  lastPayment: string;
  nextPayment: string;
  status: string;
  cutoffDate: string;
}

interface UserPreferences {
  favoriteTags: string[];
  averageCalories: number;
  preferredProteins: string[];
  totalOrders: number;
  lastOrderWeek: string;
}

interface NotificationSettings {
  recipeReminder: boolean;
  shipmentAlert: boolean;
  daysBeforeCutoff: number;  // Days before cutoff to send reminder
  lastRecipeReminder: string | null;  // ISO date
  lastShipmentAlert: string | null;   // ISO date
  lastShipmentStatus: string | null;  // Raw status text for change detection
  preferredChannel: 'telegram' | 'discord' | 'inchat';
}

interface HelloFreshNotification {
  type: 'recipe_reminder' | 'shipment_alert';
  subscriptionId: string;
  message: string;
  recipes?: string[];
  actionUrl?: string;
}

interface CachedRecipe {
  name: string;
  instructions?: string;
  cachedAt: string;
  deliveryDate?: string;
  week?: string;
  status: 'pending' | 'available' | 'failed';
  error?: string;
}

interface RecipeCache {
  [recipeName: string]: CachedRecipe;
}

interface RecipeInfo {
  name: string;
  time: string;
  cal: string;
  prot: string;
  tags: string;
}

// ============ ERROR HANDLING ============

class HelloFreshError extends Error {
  constructor(
    message: string,
    public code: 'NOT_SETUP' | 'BROWSER_ERROR' | 'PARSE_ERROR' | 'SESSION_ERROR'
  ) {
    super(message);
    this.name = 'HelloFreshError';
  }
}

function withErrorHandling<T>(fn: () => T, context: string): T {
  try {
    return fn();
  } catch (error) {
    if (error instanceof HelloFreshError) {
      throw error;
    }
    throw new HelloFreshError(`${context}: ${error instanceof Error ? error.message : 'Unknown error'}`, 'BROWSER_ERROR');
  }
}

// ============ SESSION MANAGEMENT ============

function loadSession(): Session {
  try {
    const fs = require('fs');
    if (fs.existsSync(SESSION_FILE)) {
      const data = fs.readFileSync(SESSION_FILE, 'utf-8');
      const parsed = JSON.parse(data) as Session;
      
      // Validate required fields
      if (!parsed.preferences) {
        parsed.preferences = { favoriteTags: [], averageCalories: 0, preferredProteins: [], totalOrders: 0, lastOrderWeek: '' };
      }
      if (!parsed.notifications) {
        parsed.notifications = { 
          recipeReminder: false, 
          shipmentAlert: false,
          daysBeforeCutoff: 3,
          lastRecipeReminder: null,
          lastShipmentAlert: null,
          lastShipmentStatus: null,
          preferredChannel: 'telegram'
        };
      } else {
        // Migration: add missing fields to existing notifications
        if (parsed.notifications.daysBeforeCutoff === undefined) {
          parsed.notifications.daysBeforeCutoff = 3;
        }
        if (parsed.notifications.lastRecipeReminder === undefined) {
          parsed.notifications.lastRecipeReminder = null;
        }
        if (parsed.notifications.lastShipmentAlert === undefined) {
          parsed.notifications.lastShipmentAlert = null;
        }
        if (parsed.notifications.preferredChannel === undefined) {
          parsed.notifications.preferredChannel = 'telegram';
        }
      }
      return parsed;
    }
  } catch (error) {
    console.error('Failed to load session:', error);
  }
  
  return { 
    setupComplete: false, 
    preferences: { favoriteTags: [], averageCalories: 0, preferredProteins: [], totalOrders: 0, lastOrderWeek: '' },
    notifications: { 
      recipeReminder: false, 
      shipmentAlert: false,
      daysBeforeCutoff: 3,
      lastRecipeReminder: null,
      lastShipmentAlert: null,
          lastShipmentStatus: null,
      preferredChannel: 'telegram'
    }
  };
}

function saveSession(session: Session): void {
  const fs = require('fs');
  const path = require('path');
  const dir = path.dirname(SESSION_FILE);
  
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  
  // Atomic write: write to temp file, then rename
  const tmpFile = `${SESSION_FILE}.tmp`;
  fs.writeFileSync(tmpFile, JSON.stringify(session, null, 2));
  fs.renameSync(tmpFile, SESSION_FILE);
}

// ============ RECIPE CACHE MANAGEMENT ============

function loadRecipeCache(): RecipeCache {
  try {
    const fs = require('fs');
    if (fs.existsSync(RECIPE_CACHE_FILE)) {
      return JSON.parse(fs.readFileSync(RECIPE_CACHE_FILE, 'utf-8'));
    }
  } catch (error) {
    console.error('Failed to load recipe cache:', error);
  }
  return {};
}

function saveRecipeCache(cache: RecipeCache): void {
  const fs = require('fs');
  const path = require('path');
  const dir = path.dirname(RECIPE_CACHE_FILE);
  
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
  
  const tmpFile = `${RECIPE_CACHE_FILE}.tmp`;
  fs.writeFileSync(tmpFile, JSON.stringify(cache, null, 2));
  fs.renameSync(tmpFile, RECIPE_CACHE_FILE);
}

function getCachedRecipe(name: string): CachedRecipe | null {
  const cache = loadRecipeCache();
  const normalizedName = name.toLowerCase().trim();
  return cache[normalizedName] || null;
}

function cacheRecipe(name: string, recipe: CachedRecipe): void {
  const cache = loadRecipeCache();
  const normalizedName = name.toLowerCase().trim();
  cache[normalizedName] = recipe;
  saveRecipeCache(cache);
}

function isRecipeAvailable(recipe: CachedRecipe): boolean {
  if (recipe.status !== 'available') return false;
  if (!recipe.instructions || recipe.instructions.length < 20) return false;
  return true;
}

function shouldRefetch(recipe: CachedRecipe): boolean {
  const now = new Date();
  
  // Always refetch failed recipes
  if (recipe.status === 'failed') return true;
  
  // If pending, check delivery date OR TTL
  if (recipe.status === 'pending') {
    // Check if past delivery date
    if (recipe.deliveryDate) {
      const deliveryDate = new Date(recipe.deliveryDate);
      if (!isNaN(deliveryDate.getTime()) && now > deliveryDate) {
        return true;
      }
    }
    
    // TTL fallback: refetch after 24 hours if no delivery date
    if (recipe.cachedAt) {
      const cachedTime = new Date(recipe.cachedAt);
      const hoursSinceCached = (now.getTime() - cachedTime.getTime()) / (1000 * 60 * 60);
      if (hoursSinceCached > 24) {
        return true;
      }
    }
    
    // If no cachedAt at all, refetch
    return true;
  }
  
  return false;
}

// Cache pruning - remove entries older than 90 days
function pruneOldCache(): void {
  try {
    const cache = loadRecipeCache();
    const now = new Date();
    const ninetyDaysAgo = new Date(now.getTime() - (90 * 24 * 60 * 60 * 1000));
    
    let pruned = false;
    const keysToDelete: string[] = [];
    
    for (const [key, recipe] of Object.entries(cache)) {
      if (recipe.cachedAt) {
        const cachedTime = new Date(recipe.cachedAt);
        if (cachedTime < ninetyDaysAgo) {
          keysToDelete.push(key);
          pruned = true;
        }
      }
    }
    
    if (pruned) {
      keysToDelete.forEach(key => delete cache[key]);
      saveRecipeCache(cache);
      console.log(`Pruned ${keysToDelete.length} old recipes from cache`);
    }
  } catch (error) {
    console.error('Failed to prune cache:', error);
  }
}

// Parse human date to ISO (e.g., "Mar 15" -> "2026-03-15")
function parseDeliveryDate(dateStr: string | undefined): string | undefined {
  if (!dateStr) return undefined;
  
  const currentYear = new Date().getFullYear();
  const parsed = new Date(`${dateStr} ${currentYear}`);
  
  if (!isNaN(parsed.getTime())) {
    return parsed.toISOString().split('T')[0]; // Return YYYY-MM-DD
  }
  
  return undefined;
}

// ============ WEEK HELPERS (ISO STANDARD) ============

/**
 * Get ISO week number and year
 * ISO week starts on Monday, week 1 is the first week with a Thursday
 */
function getISOWeek(date: Date): { year: number; week: number } {
  // Copy date to avoid mutation
  const d = new Date(Date.UTC(date.getFullYear(), date.getMonth(), date.getDate()));
  const dayNum = d.getUTCDay() || 7; // UTC day (0 is Sunday)
  d.setUTCDate(d.getUTCDate() + 4 - dayNum); // Set to first Thursday
  const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
  const weekNum = Math.ceil((((d.getTime() - yearStart.getTime()) / 86400000) + 1) / 7);
  return { year: d.getUTCFullYear(), week: weekNum };
}

/**
 * Get week string in HelloFresh format (YYYY-Www)
 */
function getWeekString(week?: string): string {
  const now = new Date();
  
  if (week === 'next') {
    now.setDate(now.getDate() + 7);
  } else if (week === 'last') {
    now.setDate(now.getDate() - 7);
  }
  
  const { year, week: weekNum } = getISOWeek(now);
  return `${year}-W${weekNum.toString().padStart(2, '0')}`;
}

// ============ HELPER FUNCTIONS ============

function extractRecipeInfo(html: string, limit?: number): RecipeInfo[] {
  const recipes: RecipeInfo[] = [];
  let match;
  const regex = new RegExp(PATTERNS.recipe.source, 'gi');
  
  while ((match = regex.exec(html)) !== null) {
    if (limit && recipes.length >= limit) break;
    
    recipes.push({
      name: match[1],
      time: match[2],
      cal: match[3],
      prot: match[4],
      tags: ''
    });
  }
  
  // Extract tags
  const tagRegex = new RegExp(PATTERNS.recipeTag.source, 'gi');
  let tagMatch;
  while ((tagMatch = tagRegex.exec(html)) !== null) {
    const tag = tagMatch[1];
    const recName = tagMatch[2];
    const rec = recipes.find(r => r.name === recName);
    if (rec) {
      rec.tags += (rec.tags ? ', ' : '') + tag;
    }
  }
  
  return recipes;
}

function wait(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// ============ COMMAND HANDLERS ============

// /hello-fresh status
export function cmdStatus(): string {
  return withErrorHandling(() => {
    const session = loadSession();
    
    if (!session.setupComplete) {
      return '❌ Not set up. Run `/hello-fresh setup` first.';
    }
    
    const sub = session.subscription;
    if (!sub) {
      return '❌ No subscription found. Run `/hello-fresh setup`.';
    }
    
    // Check browser mode
    const useKernel = process.env.USE_KERNEL === 'true';
    const browserMode = useKernel ? '☁️ Kernel Cloud' : '🔗 Local Chrome';
    
    return `📋 **HelloFresh Status**

- **Browser:** ${browserMode}
- **Plan:** ${sub.planName}
- **Meals/box:** ${sub.mealsPerBox}
- **Delivery:** ${sub.deliveryDay}, ${sub.deliveryWindow}
- **Price:** $${sub.pricePerBox} ($${sub.pricePerServing}/serving + $${sub.shipping} shipping)
- **Address:** ${sub.deliveryAddress}
- **Status:** ${sub.status === 'active' ? '✅ Active' : sub.status}
- **Next payment:** ${sub.nextPayment}
- **Cutoff to edit:** ${sub.cutoffDate}`;
  }, 'cmdStatus');
}

// /hello-fresh discover [week]
export async function cmdDiscover(week: string): Promise<string> {
  const session = loadSession();
  
  if (!session.setupComplete || !session.subscription) {
    return '❌ Run `/hello-fresh setup` first.';
  }
  
  try {
    const weekStr = getWeekString(week || 'this');
    const url = `${BASE_URL}/my-account/deliveries/menu?subscriptionId=${session.subscription.id}&week=${weekStr}`;
    
    // Navigate to menu page
    await browser({ action: 'navigate', profile: 'chrome', targetUrl: url });
    await wait(PAGE_LOAD_TIMEOUT_MS);
    
    const snapshot = await browser({ action: 'snapshot', profile: 'chrome' });
    const html = snapshot.result?.html || '';
    
    if (!html) {
      throw new HelloFreshError('Failed to load page - empty response', 'BROWSER_ERROR');
    }
    
    // Extract delivery date
    const dateMatch = html.match(PATTERNS.deliveryDate);
    const deliveryDate = dateMatch ? dateMatch[1] : weekStr;
    
    // Extract cutoff date
    const cutoffMatch = html.match(PATTERNS.cutoffDate);
    const cutoff = cutoffMatch ? cutoffMatch[1] : 'Unknown';
    
    // Extract selected meals (first 3)
    const selectedRecipes = extractRecipeInfo(html, 3);
    const selectedNames = selectedRecipes.map(r => r.name);
    
    // Try to click "Browse more delicious meals" using text selector
    // Use act with a more robust selector approach
    try {
      await browser({ 
        action: 'act', 
        profile: 'chrome',
        request: { kind: 'click', ref: 'e382' }
      });
      await wait(PAGE_LOAD_TIMEOUT_MS);
    } catch (clickError) {
      console.log('Could not click browse button, using main page data');
    }
    
    const browseSnapshot = await browser({ action: 'snapshot', profile: 'chrome' });
    const browseHtml = browseSnapshot.result?.html || '';
    
    // Extract all available recipes
    const allRecipes = extractRecipeInfo(browseHtml);
    
    // Filter out already selected
    const availableRecipes = allRecipes.filter(r => !selectedNames.includes(r.name));
    
    // Build output
    let output = `📋 **Week of ${deliveryDate}** (Edit by ${cutoff})\n\n`;
    
    output += `**Your selected meals:**\n`;
    if (selectedRecipes.length > 0) {
      output += selectedRecipes.map((r, i) => 
        `✅ ${r.name} — ${r.time} min, ${r.cal} cal, ${r.prot}g`
      ).join('\n') + '\n\n';
    } else {
      output += `_No meals selected yet._\n\n`;
    }
    
    output += `**Available to swap:**\n`;
    if (availableRecipes.length > 0) {
      const displayRecipes = availableRecipes.slice(0, 8);
      output += displayRecipes.map((r, i) => {
        let line = `${i + 1}. ${r.name}\n   ${r.time} min | ${r.cal} cal | ${r.prot}g`;
        if (r.tags) line += ` | ${r.tags}`;
        return line;
      }).join('\n');
      
      if (availableRecipes.length > 8) {
        output += `\n\n_...and ${availableRecipes.length - 8} more in the browser_`;
      }
    } else {
      output += `_No additional recipes found._`;
    }
    
    return output;
    
  } catch (error) {
    if (error instanceof HelloFreshError) {
      return `❌ ${error.message}`;
    }
    return `❌ Error: ${error instanceof Error ? error.message : 'Unknown error'}`;
  }
}

// /hello-fresh select
export async function cmdSelect(week?: string): Promise<string> {
  const session = loadSession();
  
  if (!session.setupComplete || !session.subscription) {
    return '❌ Run `/hello-fresh setup` first.';
  }
  
  try {
    const weekStr = getWeekString(week || 'next');
    const url = `${BASE_URL}/my-account/deliveries/menu?subscriptionId=${session.subscription.id}&week=${weekStr}`;
    
    await browser({ action: 'navigate', profile: 'chrome', targetUrl: url });
    
    return `🔄 Navigated to meal selection for ${weekStr}\n\nUse the browser to change your meals, then come back here.`;
  } catch (error) {
    return `❌ Error navigating to selection: ${error instanceof Error ? error.message : 'Unknown error'}`;
  }
}

// /hello-fresh history
export async function cmdHistory(): Promise<string> {
  const session = loadSession();
  
  if (!session.setupComplete || !session.subscription) {
    return '❌ Run `/hello-fresh setup` first.';
  }
  
  try {
    const url = `${BASE_URL}/my-account/deliveries/past-deliveries?subscriptionId=${session.subscription.id}`;
    
    await browser({ action: 'navigate', profile: 'chrome', targetUrl: url });
    await wait(PAGE_LOAD_TIMEOUT_MS);
    
    const snapshot = await browser({ action: 'snapshot', profile: 'chrome' });
    const html = snapshot.result?.html || '';
    
    if (!html) {
      throw new HelloFreshError('Failed to load history page', 'BROWSER_ERROR');
    }
    
    // Parse past deliveries
    const deliveries: { date: string; recipes: string[] }[] = [];
    const deliveryMatches = [...html.matchAll(new RegExp(PATTERNS.pastDelivery.source, 'gi'))];
    
    for (let i = 0; i < deliveryMatches.length; i++) {
      const deliveryMatch = deliveryMatches[i];
      const date = deliveryMatch[1];
      const sectionStart = deliveryMatch.index || 0;
      // Section ends at next delivery or end of HTML
      const sectionEnd = (i + 1 < deliveryMatches.length) 
        ? (deliveryMatches[i + 1].index || html.length) 
        : html.length;
      const section = html.slice(sectionStart, sectionEnd);
      
      const recipes = extractRecipeInfo(section).map(r => 
        `${r.name} — ${r.time} min, ${r.cal} cal, ${r.prot}g protein`
      );
      
      if (recipes.length > 0) {
        deliveries.push({ date, recipes });
      }
    }
    
    if (deliveries.length === 0) {
      return '📦 **Past Deliveries**\n\nNo past deliveries found.';
    }
    
    // Build output
    let output = '📦 **Past Deliveries**\n\n';
    
    for (const delivery of deliveries.slice(0, 5)) {
      output += `**${delivery.date}** (${delivery.recipes.length} recipes)\n`;
      output += delivery.recipes.map(r => `• ${r}`).join('\n') + '\n\n';
    }
    
    // Calculate preferences
    const allRecipes = deliveries.flatMap(d => d.recipes);
    const beefCount = allRecipes.filter(r => r.toLowerCase().includes('beef')).length;
    const chickenCount = allRecipes.filter(r => r.toLowerCase().includes('chicken')).length;
    const tofuCount = allRecipes.filter(r => r.toLowerCase().includes('tofu') || r.toLowerCase().includes('veggie')).length;
    
    output += `📊 **Your Preferences (${allRecipes.length} orders):**\n`;
    output += `• Beef: ${beefCount} orders\n`;
    output += `• Chicken: ${chickenCount} orders\n`;
    output += `• Veggie: ${tofuCount} orders\n`;
    
    return output;
    
  } catch (error) {
    if (error instanceof HelloFreshError) {
      return `❌ ${error.message}`;
    }
    return `❌ Error: ${error instanceof Error ? error.message : 'Unknown error'}`;
  }
}

// /hello-fresh reset
export function cmdReset(): string {
  try {
    const fs = require('fs');
    if (fs.existsSync(SESSION_FILE)) {
      fs.unlinkSync(SESSION_FILE);
    }
  } catch (error) {
    return `⚠️ Error clearing session: ${error instanceof Error ? error.message : 'Unknown error'}`;
  }
  return '🔄 Session cleared. Run `/hello-fresh setup` to start over.';
}

// /hello-fresh recommend
export async function cmdRecommend(): Promise<string> {
  const session = loadSession();
  
  if (!session.setupComplete || !session.subscription) {
    return '❌ Run `/hello-fresh setup` first.';
  }
  
  try {
    // First, get history to analyze preferences
    const url = `${BASE_URL}/my-account/deliveries/past-deliveries?subscriptionId=${session.subscription.id}`;
    await browser({ action: 'navigate', profile: 'chrome', targetUrl: url });
    await wait(PAGE_LOAD_TIMEOUT_MS);
    const snapshot = await browser({ action: 'snapshot', profile: 'chrome' });
    const html = snapshot.result?.html || '';
    
    if (!html) {
      throw new HelloFreshError('Failed to load history', 'BROWSER_ERROR');
    }
    
    // Parse deliveries for preferences
    const deliveries: { date: string; recipes: RecipeInfo[] }[] = [];
    const deliveryMatches = [...html.matchAll(new RegExp(PATTERNS.pastDelivery.source, 'gi'))];
    
    for (let i = 0; i < deliveryMatches.length; i++) {
      const deliveryMatch = deliveryMatches[i];
      const date = deliveryMatch[1];
      const sectionStart = deliveryMatch.index || 0;
      const sectionEnd = (i + 1 < deliveryMatches.length) 
        ? (deliveryMatches[i + 1].index || html.length) 
        : html.length;
      const section = html.slice(sectionStart, sectionEnd);
      
      const recipes = extractRecipeInfo(section);
      if (recipes.length > 0) {
        deliveries.push({ date, recipes });
      }
    }
    
    if (deliveries.length === 0) {
      return '📝 No order history yet. After a few orders, I can make recommendations!';
    }
    
    // Analyze preferences
    const allRecipes = deliveries.flatMap(d => d.recipes);
    const allNames = allRecipes.map(r => r.name.toLowerCase());
    const allTags = allRecipes.flatMap(r => r.tags.split(', ').filter(Boolean));
    
    // Count preferences
    const proteinPrefs = {
      beef: allNames.filter(n => n.includes('beef')).length,
      chicken: allNames.filter(n => n.includes('chicken')).length,
      pork: allNames.filter(n => n.includes('pork')).length,
      tofu: allNames.filter(n => n.includes('tofu')).length,
      shrimp: allNames.filter(n => n.includes('shrimp')).length,
      salmon: allNames.filter(n => n.includes('salmon')).length,
    };
    
    const tagPrefs: Record<string, number> = {};
    allTags.forEach(tag => {
      tagPrefs[tag] = (tagPrefs[tag] || 0) + 1;
    });
    const topTags = Object.entries(tagPrefs)
      .sort((a, b) => b[1] - a[1])
      .slice(0, 5)
      .map(([tag]) => tag);
    
    const topProtein = Object.entries(proteinPrefs)
      .sort((a, b) => b[1] - a[1])[0];
    
    // Get current week's available recipes
    const currentWeek = getWeekString('this');
    const menuUrl = `${BASE_URL}/my-account/deliveries/menu?subscriptionId=${session.subscription.id}&week=${currentWeek}`;
    await browser({ action: 'navigate', profile: 'chrome', targetUrl: menuUrl });
    await wait(PAGE_LOAD_TIMEOUT_MS);
    const menuSnapshot = await browser({ action: 'snapshot', profile: 'chrome' });
    const menuHtml = menuSnapshot.result?.html || '';
    
    // Extract available recipes
    const availableRecipes = extractRecipeInfo(menuHtml, 20);
    
    // Score and rank recipes
    const scoredRecipes = availableRecipes.map(r => {
      let score = 0;
      const name = r.name.toLowerCase();
      const tags = r.tags.toLowerCase();
      
      // Protein match
      if (name.includes(topProtein[0])) score += 5;
      
      // Tag matches
      topTags.forEach(tag => {
        if (tags.includes(tag.toLowerCase())) score += 2;
      });
      
      // Quick meals bonus (if user prefers quick)
      if (topTags.includes('Quick') && (name.includes('quick') || tags.includes('quick'))) score += 3;
      
      // Calorie awareness (if health-conscious)
      if (topTags.includes('High Protein') && parseInt(r.prot) > 40) score += 2;
      
      return { ...r, score };
    }).sort((a, b) => b.score - a.score);
    
    const recommendations = scoredRecipes.slice(0, 5);
    
    // Build output
    let output = `🤖 **Recommendations based on ${allRecipes.length} orders**\n\n`;
    output += `**Your preferences:**\n`;
    output += `• Favorite protein: ${topProtein[0]} (${topProtein[1]} orders)\n`;
    output += `• Top tags: ${topTags.join(', ')}\n\n`;
    
    output += `**Top picks for this week:**\n`;
    recommendations.forEach((r, i) => {
      output += `${i + 1}. **${r.name}**\n`;
      output += `   ${r.time} min | ${r.cal} cal | ${r.prot}g protein`;
      if (r.tags) output += ` | ${r.tags}`;
      output += `\n`;
    });
    
    return output;
    
  } catch (error) {
    if (error instanceof HelloFreshError) {
      return `❌ ${error.message}`;
    }
    return `❌ Error: ${error instanceof Error ? error.message : 'Unknown error'}`;
  }
}

// /hello-fresh convert <recipe>
export async function cmdConvert(recipeName: string): Promise<string> {
  // Prune old cache entries on each call
  pruneOldCache();
  
  const session = loadSession();
  
  if (!session.setupComplete || !session.subscription) {
    return '❌ Run `/hello-fresh setup` first.';
  }
  
  if (!recipeName) {
    return 'Usage: `/hello-fresh convert <recipe-name>`\nExample: `/hello-fresh convert Cheesy Beef Taquitos`';
  }
  
  // ===== CHECK CACHE FIRST =====
  const cached = getCachedRecipe(recipeName);
  
  if (cached && isRecipeAvailable(cached)) {
    // Return cached instructions via TTS
    const instructions = cached.instructions || '';
    if (!instructions) {
      return `❌ No instructions found for "${recipeName}". Try fetching fresh.`;
    }
    
    const speechText = `Cooking ${recipeName}. ${instructions}`.slice(0, 5000); // Max 5000 chars
    try {
      await tts({ text: speechText });
    } catch (e) {
      console.error('TTS error:', e);
      return `🔊 **Cooking Instructions for ${recipeName}**\n\n${instructions}`;
    }
    return `🔊 Playing cooking instructions for "${recipeName}"...`;
  }
  
  if (cached && !shouldRefetch(cached)) {
    // Still pending - tell user when to retry
    const retryMsg = cached.deliveryDate 
      ? `Try again after ${cached.deliveryDate} when your box arrives!`
      : 'The recipe is not yet available. Try again after your delivery.';
    
    return `📦 **Recipe: ${recipeName}**

⏳ Status: Not yet available
${retryMsg}

_Cached from previous attempt: ${cached.cachedAt}_`;
  }
  
  // ===== FETCH FROM REMOTE =====
  try {
    // Navigate to the menu page where recipes are displayed
    const menuUrl = `${BASE_URL}/my-account/deliveries/menu?subscriptionId=${session.subscription.id}`;
    await browser({ action: 'navigate', profile: 'chrome', targetUrl: menuUrl });
    await wait(PAGE_LOAD_TIMEOUT_MS);
    
    const snapshot = await browser({ action: 'snapshot', profile: 'chrome' });
    const html = snapshot.result?.html || '';
    
    // Look for the recipe button in the page
    const escapedName = recipeName.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    
    // Try to find the ref for the recipe button
    const headingRefMatch = html.match(new RegExp(`heading\\s+"${escapedName}"[^>]*\\[ref=([^\\]]+)\\]`, 'i'));
    
    let clicked = false;
    if (headingRefMatch && headingRefMatch[1]) {
      try {
        await browser({ 
          action: 'act', 
          profile: 'chrome',
          request: { kind: 'click', ref: headingRefMatch[1] }
        });
        clicked = true;
      } catch (e) {
        // Try clicking by text
      }
    }
    
    // If not clicked yet, try finding any button containing the recipe name
    if (!clicked) {
      const buttonMatch = html.match(new RegExp(`button[^>]*>[^<]*${escapedName}`, 'i'));
      if (buttonMatch) {
        const refMatch = buttonMatch[0].match(/\[ref=([^\]]+)\]/);
        if (refMatch) {
          await browser({ 
            action: 'act', 
            profile: 'chrome',
            request: { kind: 'click', ref: refMatch[1] }
          });
          clicked = true;
        }
      }
    }
    
    // Wait for modal to open
    await wait(2000);
    
    // Get the modal content
    const modalSnapshot = await browser({ action: 'snapshot', profile: 'chrome' });
    const modalHtml = modalSnapshot.result?.html || '';
    
    // Check if recipe is not yet available
    const notAvailablePatterns = [
      /full recipe coming soon/i,
      /recipe available after/i,
      /cooking instructions will be available/i,
    ];
    
    for (const pattern of notAvailablePatterns) {
      if (pattern.test(modalHtml)) {
        // Extract delivery date for context and convert to ISO
        const deliveryMatch = html.match(/Sun\.\s+(\w+\s+\d+)/i);
        const deliveryDateRaw = deliveryMatch ? deliveryMatch[1] : undefined;
        const deliveryDateISO = parseDeliveryDate(deliveryDateRaw);
        
        // Cache as pending
        cacheRecipe(recipeName, {
          name: recipeName,
          cachedAt: new Date().toISOString(),
          deliveryDate: deliveryDateISO,
          status: 'pending'
        });
        
        return `📦 **Recipe: ${recipeName}**

⏳ Status: Not yet available

📝 HelloFresh only publishes the full recipe after your box is delivered.
   The recipe card with instructions will be included in your box.

💡 ${deliveryDateRaw ? `Try again after ${deliveryDateRaw}` : 'Try again after your delivery'} when you receive your ingredients!

_(Cached - I'll check again automatically when you retry)_`;
      }
    }
    
    // Try to extract cooking instructions from the modal
    const instructionSectionPatterns = [
      /instructions?[^>]*>([\s\S]*?)<\/[^>]+>/i,
      /cooking-?steps?[^>]*>([\s\S]*?)<\/[^>]+>/i,
      /method[^>]*>([\s\S]*?)<\/[^>]+>/i,
      /directions?[^>]*>([\s\S]*?)<\/[^>]+>/i,
    ];
    
    let instructions = '';
    for (const pattern of instructionSectionPatterns) {
      const match = modalHtml.match(pattern);
      if (match && match[1] && match[1].length > 50) {
        const steps = [...match[1].matchAll(/<li[^>]*>([^<]+)<\/li>/gi)];
        if (steps.length > 0) {
          instructions = steps.map(s => s[1].replace(/<[^>]+>/g, '').trim()).join('. ');
          break;
        }
      }
    }
    
    // Try ordered list as fallback
    if (!instructions || instructions.length < 20) {
      const olMatch = modalHtml.match(/<ol[^>]*>([\s\S]*?)<\/ol>/i);
      if (olMatch) {
        const steps = [...olMatch[1].matchAll(/<li[^>]*>([^<]+)<\/li>/gi)];
        if (steps.length > 0) {
          instructions = steps.map(s => s[1].replace(/<[^>]+>/g, '').trim()).join('. ');
        }
      }
    }
    
    if (instructions && instructions.length > 20) {
      // Cache the recipe
      cacheRecipe(recipeName, {
        name: recipeName,
        instructions: instructions,
        cachedAt: new Date().toISOString(),
        status: 'available'
      });
      
      const speechText = `Cooking ${recipeName}. ${instructions}`.slice(0, 5000); // Max 5000 chars
      
      // Cache and play via TTS
      try {
        await tts({ text: speechText });
      } catch (e) {
        console.error('TTS error:', e);
        // Mark cache as failed so it retries later
        cacheRecipe(recipeName, {
          name: recipeName,
          instructions: instructions,
          cachedAt: new Date().toISOString(),
          status: 'failed',
          error: 'TTS failed'
        });
        return `🔊 **Cooking Instructions for ${recipeName}**\n\n${instructions}`;
      }
      return `🔊 Playing cooking instructions for "${recipeName}"...`;
    }
    
    // Close modal
    try {
      await browser({ 
        action: 'act', 
        profile: 'chrome',
        request: { kind: 'press', key: 'Escape' }
      });
    } catch (e) {
      // Ignore
    }
    
    // Cache as failed (will retry on next attempt)
    cacheRecipe(recipeName, {
      name: recipeName,
      cachedAt: new Date().toISOString(),
      status: 'failed',
      error: 'Could not extract instructions'
    });
    
    return `🔊 Could not extract cooking instructions for "${recipeName}".\n\n` +
      `The recipe modal may not have loaded properly, or the instructions aren't available yet.\n` +
      `Try again after your delivery date.`;
    
  } catch (error) {
    return `❌ Error: ${error instanceof Error ? error.message : 'Unknown error'}`;
  }
}

// /hello-fresh track
export async function cmdTrack(): Promise<string> {
  const session = loadSession();
  
  if (!session.setupComplete || !session.subscription) {
    return '❌ Run `/hello-fresh setup` first.';
  }
  
  try {
    // Get current week's delivery
    const currentWeek = getWeekString('this');
    const url = `${BASE_URL}/my-account/deliveries/menu?subscriptionId=${session.subscription.id}&week=${currentWeek}`;
    
    await browser({ action: 'navigate', profile: 'chrome', targetUrl: url });
    await wait(PAGE_LOAD_TIMEOUT_MS);
    const snapshot = await browser({ action: 'snapshot', profile: 'chrome' });
    const html = snapshot.result?.html || '';
    
    // Look for tracking link
    const trackingMatch = html.match(/delivery-tracking\/([a-f0-9-]+)/i);
    const statusMatch = html.match(/status["\s:]+([^<\n]+)/i);
    
    if (trackingMatch) {
      const trackingUrl = `${BASE_URL}/delivery-tracking/${trackingMatch[1]}`;
      await browser({ action: 'navigate', profile: 'chrome', targetUrl: trackingUrl });
      await wait(PAGE_LOAD_TIMEOUT_MS);
      
      const trackSnapshot = await browser({ action: 'snapshot', profile: 'chrome' });
      const trackHtml = trackSnapshot.result?.html || '';
      
      // Extract tracking info
      const statusPattern = /(delivered|out for delivery|preparing|shipped|ordered)/i;
      const statusMatch = trackHtml.match(statusPattern);
      const etaMatch = trackHtml.match(/eta[:\s]+([^<\n]+)/i);
      
      let output = `🚚 **Delivery Tracking**\n\n`;
      
      if (statusMatch) {
        output += `**Status:** ${statusMatch[1].charAt(0).toUpperCase() + statusMatch[1].slice(1)}\n`;
      }
      if (etaMatch) {
        output += `**ETA:** ${etaMatch[1].trim()}\n`;
      }
      
      output += `\n_Opened tracking page in browser._`;
      return output;
    }
    
    // Check if delivery is upcoming
    const dateMatch = html.match(PATTERNS.deliveryDate);
    const deliveryDate = dateMatch ? dateMatch[1] : 'Unknown';
    
    return `📦 **Delivery Status**\n\n**Scheduled for:** ${deliveryDate}\n\nTracking not yet available. Usually appears the day before delivery.`;
    
  } catch (error) {
    return `❌ Error: ${error instanceof Error ? error.message : 'Unknown error'}`;
  }
}

// ============ NOTIFICATION FUNCTIONS ============

// Check if we should send recipe reminder
function shouldSendRecipeReminder(session: Session): boolean {
  if (!session.notifications?.recipeReminder) return false;
  if (!session.subscription?.cutoffDate) return false;
  
  const cutoffDate = new Date(session.subscription.cutoffDate);
  // Invalid date check
  if (isNaN(cutoffDate.getTime())) {
    console.warn('Invalid cutoff date:', session.subscription.cutoffDate);
    return false;
  }
  
  const now = new Date();
  const daysBefore = session.notifications.daysBeforeCutoff ?? 3;  // Use ?? to allow 0
  
  // Check if we're within the notification window (including cutoff day)
  const daysUntilCutoff = Math.ceil((cutoffDate.getTime() - now.getTime()) / (1000 * 60 * 60 * 24));
  
  if (daysUntilCutoff <= daysBefore && daysUntilCutoff >= 0) {
    // Check if we already notified today
    const lastNotified = session.notifications.lastRecipeReminder;
    if (lastNotified) {
      const lastDate = new Date(lastNotified);
      const today = new Date();
      if (lastDate.toDateString() === today.toDateString()) {
        return false; // Already notified today
      }
    }
    return true;
  }
  
  return false;
}

// Check if we should send shipment alert using the new tracking system
async function shouldSendShipmentAlert(session: Session): Promise<{shouldNotify: boolean; message?: string}> {
  if (!session.notifications?.shipmentAlert) {
    return { shouldNotify: false };
  }
  
  try {
    const result = await checkShipmentAlert();
    
    if (!result.shipment) {
      return { shouldNotify: false };
    }
    
    if (result.shouldNotify) {
      let message = `📦 **HelloFresh Shipment Update**\n\n`;
      
      if (result.previousStatus) {
        message += `Status changed:\n`;
        message += `• Previous: ${result.previousStatus}\n`;
        message += `• Current: ${result.shipment.statusRaw}\n\n`;
      } else {
        message += `New shipment detected!\n`;
        message += `${result.shipment.statusRaw}\n\n`;
      }
      
      message += `**${result.shipment.meals} meals** on ${result.shipment.deliveryDate}`;
      
      return { shouldNotify: true, message };
    }
    
    return { shouldNotify: false };
  } catch (error) {
    console.error('Error checking shipment alert:', error);
    return { shouldNotify: false };
  }
}

// Send notification via preferred channel
async function sendNotification(message: string, channel?: string): Promise<string> {
  // In a real implementation, this would use the message tool
  // For now, return the message that would be sent
  return `📤 **Notification would be sent:**\n\n${message}\n\nChannel: ${channel || 'telegram'}`;
}

// /hello-fresh notify - check and send notifications
export async function cmdNotify(action?: string): Promise<string> {
  const session = loadSession();
  
  if (!session.setupComplete) {
    return '❌ Run `/hello-fresh setup` first.';
  }
  
  // Handle sub-commands
  if (action === 'test') {
    return await sendNotification('🔔 Test notification from HelloFresh Skill!', session.notifications?.preferredChannel);
  }
  
  if (action === 'settings') {
    const notif = session.notifications;
    return `⚙️ **Notification Settings**

- **Recipe Reminders:** ${notif?.recipeReminder ? '✅ Enabled' : '❌ Disabled'}
- **Shipment Alerts:** ${notif?.shipmentAlert ? '✅ Enabled' : '❌ Disabled'}
- **Days before cutoff:** ${notif?.daysBeforeCutoff || 3} days
- **Preferred channel:** ${notif?.preferredChannel || 'telegram'}
- **Last recipe reminder:** ${notif?.lastRecipeReminder || 'Never'}
- **Last shipment alert:** ${notif?.lastShipmentAlert || 'Never'}

_To change settings, edit session.json or run \`/hello-fresh reset\` and set up again._`;
  }
  
  if (action === 'enable') {
    try {
      session.notifications.recipeReminder = true;
      session.notifications.shipmentAlert = true;
      saveSession(session);
      return '✅ Notifications enabled!';
    } catch (error) {
      return `❌ Error enabling notifications: ${error instanceof Error ? error.message : 'Unknown error'}`;
    }
  }
  
  if (action === 'disable') {
    try {
      session.notifications.recipeReminder = false;
      session.notifications.shipmentAlert = false;
      saveSession(session);
      return '❌ Notifications disabled.';
    } catch (error) {
      return `❌ Error disabling notifications: ${error instanceof Error ? error.message : 'Unknown error'}`;
    }
  }
  
  // Check shipment status manually
  if (action === 'check') {
    try {
      const result = await checkShipmentAlert();
      
      if (!result.shipment) {
        return '❌ Could not fetch shipment status. Make sure you\'re logged in.';
      }
      
      let output = `📦 **Current Shipment Status**\n\n`;
      output += `**Week:** ${result.shipment.week}\n`;
      output += `**Status:** ${result.shipment.statusRaw}\n`;
      output += `**Meals:** ${result.shipment.meals}\n`;
      output += `**Delivery:** ${result.shipment.deliveryDate}\n`;
      output += `\n_Last checked: ${result.shipment.checkedAt}_`;
      
      if (result.previousStatus) {
        if (result.shouldNotify) {
          output += `\n\n⚠️ **Status changed!** Previous: ${result.previousStatus}`;
        } else {
          output += `\n\n✅ No change from last check.`;
        }
      } else {
        output += `\n\n✅ First check - status saved for future comparisons.`;
      }
      
      return output;
    } catch (error) {
      return `❌ Error checking shipment: ${error instanceof Error ? error.message : 'Unknown error'}`;
    }
  }
  
  // Default: check and send notifications
  let output = '🔔 **Checking notifications...**\n\n';
  let sent = false;
  
  // Check recipe reminder
  if (shouldSendRecipeReminder(session)) {
    const daysUntilCutoff = Math.ceil((new Date(session.subscription!.cutoffDate!).getTime() - Date.now()) / (1000 * 60 * 60 * 24));
    
    const message = `📝 **Recipe Reminder!** ${daysUntilCutoff} days left to select your meals for next week!\n\n` +
      `Cutoff: ${session.subscription?.cutoffDate}\n` +
      `Run \`/hello-fresh discover\` to see available recipes.`;
    
    output += await sendNotification(message, session.notifications?.preferredChannel) + '\n\n';
    
    // Update last notified
    session.notifications.lastRecipeReminder = new Date().toISOString();
    saveSession(session);
    sent = true;
  } else {
    output += '✅ No recipe reminder needed right now.\n';
  }
  
  // Check shipment alert
  const shipmentResult = await shouldSendShipmentAlert(session);
  if (shipmentResult.shouldNotify) {
    output += await sendNotification(shipmentResult.message || '📦 Your HelloFresh box is on its way!', session.notifications?.preferredChannel);
    session.notifications.lastShipmentAlert = new Date().toISOString();
    saveSession(session);
    sent = true;
  } else {
    output += '✅ No shipment alert right now.';
  }
  
  return output;
}

// ============ MAIN ROUTER ============

export async function handleHelloFresh(args: string[]): Promise<string> {
  const cmd = args[0] || 'help';
  
  switch (cmd) {
    case 'status':
      return cmdStatus();
      
    case 'discover':
      return await cmdDiscover(args[1]);
      
    case 'select':
      return await cmdSelect(args[1]);
      
    case 'history':
      return await cmdHistory();
      
    case 'recommend':
      return await cmdRecommend();
      
    case 'convert':
      return await cmdConvert(args.slice(1).join(' '));
      
    case 'track':
      return await cmdTrack();
      
