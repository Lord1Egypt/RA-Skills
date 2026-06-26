/**
 * Skill: B2B + B2C Outreach & Lead Tracker
 * Template: lead-generation
 *
 * Automate personalized outreach (LinkedIn, DM, email) and save leads to a
 * local JSON file.  Users can list leads in chat or export them as a CSV.
 * (CRM / Supabase sync is available on paid plans.)
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const WORKSPACE_DIR = process.env.OPENCLAW_WORKSPACE || '/root/.openclaw/workspace';
const LEADS_FILE    = path.join(WORKSPACE_DIR, 'leads.json');
const CSV_FILE      = path.join(WORKSPACE_DIR, 'leads.csv');

function loadLeads() {
  try {
    if (fs.existsSync(LEADS_FILE)) {
      return JSON.parse(fs.readFileSync(LEADS_FILE, 'utf8'));
    }
  } catch { /* ignore parse errors */ }
  return [];
}

function saveLeads(leads) {
  fs.mkdirSync(WORKSPACE_DIR, { recursive: true });
  fs.writeFileSync(LEADS_FILE, JSON.stringify(leads, null, 2), 'utf8');
}

/**
 * Generate a personalized outreach message for a prospect
 * @param {object} prospect - Prospect details
 */
export async function generateOutreach(prospect) {
  try {
    if (!prospect || !prospect.name) {
      throw new Error('Prospect name is required');
    }

    const { name, company, role, recentNews, painPoint } = prospect;

    // Build personalization hooks
    const hooks = [];
    if (recentNews) hooks.push(`Recent news: ${recentNews}`);
    if (painPoint) hooks.push(`Likely pain point: ${painPoint}`);

    const sequence = [
      {
        step: 1,
        day: 'Day 1',
        type: 'connection-request',
        template: `Hi ${name}, I noticed ${recentNews || `your work at ${company || 'your company'}`}. Would love to connect — I work with ${role || 'teams'} on [your value prop]. No pitch, just genuinely interested in what you're building.`,
        maxLength: 300
      },
      {
        step: 2,
        day: 'Day 3',
        type: 'follow-up-value',
        template: `Hey ${name}, thanks for connecting! Thought you might find this useful — [relevant resource/case study]. We helped a similar ${company ? 'company' : 'team'} achieve [specific result]. Happy to share more details if interesting.`,
        maxLength: null
      },
      {
        step: 3,
        day: 'Day 7',
        type: 'soft-ask',
        template: `Hi ${name}, quick question — are you currently looking to improve [pain point area]? We've been getting great results with ${role || 'leaders'} in your space. Worth a 15-min chat?`,
        maxLength: null
      },
      {
        step: 4,
        day: 'Day 14',
        type: 'breakup',
        template: `Hey ${name}, I know you're busy so I'll keep this short. If [your solution] isn't a priority right now, totally understand. If timing changes, I'm here. Best of luck with everything at ${company || 'your company'}! 🙌`,
        maxLength: null
      }
    ];

    return {
      success: true,
      data: {
        prospect: { name, company, role },
        personalization: hooks,
        sequence,
        timestamp: new Date().toISOString()
      },
      summary: `📧 Generated 4-step outreach sequence for ${name}${company ? ` at ${company}` : ''}`
    };

  } catch (error) {
    return {
      success: false,
      error: error.message
    };
  }
}

/**
 * Score a lead based on ICP fit
 * @param {object} lead - Lead details to score
 */
export function scoreLead(lead) {
  let score = 0;
  const reasons = [];

  // Company size
  if (lead.companySize >= 50 && lead.companySize <= 500) {
    score += 20;
    reasons.push('Sweet spot company size (50-500)');
  } else if (lead.companySize > 500) {
    score += 10;
    reasons.push('Enterprise (may have longer sales cycle)');
  }

  // Decision maker title
  const dmTitles = ['ceo', 'cto', 'vp', 'head of', 'director', 'founder'];
  if (lead.title && dmTitles.some(t => lead.title.toLowerCase().includes(t))) {
    score += 25;
    reasons.push('Decision maker title');
  }

  // Industry match
  if (lead.industryMatch) {
    score += 20;
    reasons.push('Target industry match');
  }

  // Recent funding
  if (lead.recentFunding) {
    score += 15;
    reasons.push('Recently raised funding (budget available)');
  }

  // Hiring signals
  if (lead.hiringForRole) {
    score += 15;
    reasons.push('Hiring for relevant role (active need)');
  }

  // Engaged with content
  if (lead.engagedWithContent) {
    score += 10;
    reasons.push('Engaged with our content (warm lead)');
  }

  // Determine tier
  let tier;
  if (score >= 70) tier = '🔥 HOT';
  else if (score >= 40) tier = '🟡 WARM';
  else tier = '🔵 COLD';

  return {
    score,
    maxScore: 105,
    tier,
    reasons,
    recommendation: score >= 70
      ? 'Immediate outreach — high priority'
      : score >= 40
        ? 'Add to outreach sequence'
        : 'Add to nurture list',
    summary: `${tier} Lead: ${lead.name || 'Unknown'} — Score: ${score}/105`
  };
}

/**
 * Save a lead to the local leads.json file
 * @param {object} lead - Lead details
 */
export function saveLeadToFile(lead) {
  const leads = loadLeads();
  const entry = {
    id: `lead_${Date.now()}`,
    ...lead,
    source: lead.source || 'agent',
    savedAt: new Date().toISOString(),
    interactions: [],
  };
  leads.push(entry);
  saveLeads(leads);
  return {
    success: true,
    id: entry.id,
    summary: `✅ Lead saved locally: ${lead.name || 'Unknown'} (ID: ${entry.id}). Total leads: ${leads.length}. Type "show my leads" or ask me to export CSV to download.`
  };
}

/**
 * Placeholder kept for API compatibility - CRM sync available on paid plans
 */
export function formatForCRM(lead, crmType = 'hubspot') {
  return {
    success: false,
    error: 'CRM sync (HubSpot, Pipedrive, Salesforce) is available on paid plans. Use saveLeadToFile() to save locally, or export-csv to download leads.',
    crmType,
  };
}



// =============================================
// B2C FUNCTIONS
// =============================================

/**
 * Generate a B2C DM / email outreach sequence for a consumer lead
 * @param {object} consumer - Consumer details
 */
export async function generateB2COutreach(consumer) {
  try {
    if (!consumer || !consumer.name) {
      throw new Error('Consumer name is required');
    }

    const { name, platform, interest, referredBy, cartValue } = consumer;

    const sequence = [
      {
        step: 1,
        day: 'Instant',
        channel: 'email',
        type: 'welcome',
        template: `Hey ${name}! 👋 Welcome aboard. Here's the [freebie/guide/discount] we promised. Hope it's useful — reply if you have any questions!`,
      },
      {
        step: 2,
        day: 'Day 1',
        channel: 'email',
        type: 'brand-story',
        template: `Hi ${name}, quick story — we built [product] because [founder pain point]. ${interest ? `Since you're into ${interest}, you'll love this: [specific feature].` : 'Here\'s what makes us different: [differentiator].'} - [Founder Name]`,
      },
      {
        step: 3,
        day: 'Day 3',
        channel: platform || 'email',
        type: 'social-proof',
        template: `${name}, people like you are saying:\n\n⭐ "[Testimonial 1]"\n⭐ "[Testimonial 2]"\n\n${cartValue ? `Your cart (\$${cartValue}) is still waiting — ` : ''}Ready to give it a try?`,
      },
      {
        step: 4,
        day: 'Day 5',
        channel: 'email',
        type: 'offer',
        template: `Hey ${name}, we don't do this often — but here's [X% off / free trial / bonus] just for you. ${referredBy ? `(Thanks ${referredBy} for the intro!)` : ''} Valid for 48 hours. [Link]`,
      },
      {
        step: 5,
        day: 'Day 7',
        channel: 'email',
        type: 'urgency',
        template: `Last chance, ${name}! Your [discount/offer] expires tonight. After that, it's back to full price. No pressure — but didn't want you to miss out. [Link]`,
      },
    ];

    return {
      success: true,
      data: {
        consumer: { name, platform, interest },
        sequence,
        timestamp: new Date().toISOString(),
      },
      summary: `📱 Generated 5-step B2C sequence for ${name} (${platform || 'email'})`,
    };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

/**
 * Score a B2C consumer lead based on engagement signals
 * @param {object} consumer - Consumer engagement data
 */
export function scoreConsumerLead(consumer) {
  let score = 0;
  const reasons = [];

  // Website engagement
  if (consumer.visitedPricingPage) {
    score += 25;
    reasons.push('Visited pricing page (high intent)');
  }

  // Cart / trial signals
  if (consumer.addedToCart || consumer.startedTrial) {
    score += 30;
    reasons.push(consumer.addedToCart ? 'Added to cart' : 'Started free trial');
  }

  // Abandoned cart
  if (consumer.abandonedCart) {
    score += 25;
    reasons.push('Abandoned cart (was close to buying)');
  }

  // Email engagement
  if (consumer.emailOpens >= 3) {
    score += 15;
    reasons.push(`Opened ${consumer.emailOpens} emails`);
  }

  // Clicked a CTA
  if (consumer.clickedCTA) {
    score += 20;
    reasons.push('Clicked CTA link');
  }

  // Social engagement
  if (consumer.socialEngagement) {
    score += 10;
    reasons.push('Engaged on social (liked/commented)');
  }

  // Referral
  if (consumer.referredBy) {
    score += 20;
    reasons.push('Referred by existing customer');
  }

  // Demographic match
  if (consumer.matchesDemographic) {
    score += 15;
    reasons.push('Matches target demographic');
  }

  let tier;
  if (score >= 70) tier = '🔥 HOT';
  else if (score >= 40) tier = '🟡 WARM';
  else tier = '🔵 COLD';

  return {
    score,
    maxScore: 160,
    tier,
    reasons,
    recommendation:
      score >= 70
        ? 'Trigger discount/offer NOW — high purchase intent'
        : score >= 40
          ? 'Nurture sequence + retargeting ads'
          : 'Awareness content + social ads',
    summary: `${tier} Consumer: ${consumer.name || 'Unknown'} — Score: ${score}/160`,
  };
}

/**
 * Export all leads to a CSV file
 * @returns {object} result with file path
 */
export function exportLeadsAsCSV() {
  const leads = loadLeads();
  if (leads.length === 0) {
    return { success: false, error: 'No leads saved yet. Add leads first with add-lead command.' };
  }

  // Build CSV — collect all unique keys across leads
  const allKeys = [...new Set(leads.flatMap(l => Object.keys(l).filter(k => k !== 'interactions')))];
  const escape = (v) => `"${String(v ?? '').replace(/"/g, '""')}"`;

  const header = allKeys.join(',');
  const rows = leads.map(lead =>
    allKeys.map(k => escape(Array.isArray(lead[k]) ? lead[k].join('; ') : lead[k])).join(',')
  );

  const csv = [header, ...rows].join('\n');
  fs.mkdirSync(WORKSPACE_DIR, { recursive: true });
  fs.writeFileSync(CSV_FILE, csv, 'utf8');

  return {
    success: true,
    filePath: CSV_FILE,
    count: leads.length,
    summary: `📥 Exported ${leads.length} lead(s) to ${CSV_FILE}\nDownload this file to get your leads.`,
  };
}

/**
 * Placeholder — email platform sync (Klaviyo, Mailchimp, Brevo) available on paid plans
 */
export function formatForEmailPlatform(consumer, platform = 'klaviyo') {
  return {
    success: false,
    error: `Email platform sync (${platform}) is available on paid plans. Use export-csv to download leads locally.`,
  };
}

// =============================================
// CLI ENTRY POINT
// =============================================
if (process.argv[1] && fileURLToPath(import.meta.url) === path.resolve(process.argv[1])) {
  const [,, cmd, ...rest] = process.argv;

  const parseArgs = (args) => {
    const result = {};
    for (let i = 0; i < args.length; i++) {
      if (args[i].startsWith('--')) {
        const key = args[i].slice(2);
        result[key] = args[i + 1] && !args[i + 1].startsWith('--') ? args[++i] : true;
      }
    }
    return result;
  };

  switch (cmd) {
    case 'add-lead': {
      const data = parseArgs(rest);
      if (!data.name) { console.error('Error: --name is required'); process.exit(1); }
      const result = saveLeadToFile(data);
      console.log(result.summary);
      break;
    }
    case 'list': {
      const leads = loadLeads();
      if (leads.length === 0) {
        console.log('No leads saved yet.');
      } else {
        console.log(`\n📋 ${leads.length} lead(s):\n`);
        leads.forEach((l, i) => {
          console.log(`${i + 1}. [${l.id}] ${l.name || 'Unknown'} | Source: ${l.source || '-'} | Handle: ${l.handle || '-'} | Score: ${l.score || '-'} | Tier: ${l.tier || '-'}`);
          if (l.interactions?.length) console.log(`   Interactions: ${l.interactions.join(' | ')}`);
        });
      }
      break;
    }
    case 'log': {
      const [leadId, ...noteParts] = rest;
      const note = noteParts.join(' ');
      if (!leadId || !note) { console.error('Usage: log <lead_id> "note"'); process.exit(1); }
      const leads = loadLeads();
      const lead = leads.find(l => l.id === leadId);
      if (!lead) { console.error(`Lead ${leadId} not found`); process.exit(1); }
      lead.interactions = lead.interactions || [];
      lead.interactions.push(`[${new Date().toISOString()}] ${note}`);
      saveLeads(leads);
      console.log(`✅ Logged interaction for ${lead.name}: ${note}`);
      break;
    }
    case 'export-csv': {
      const result = exportLeadsAsCSV();
      console.log(result.summary || result.error);
      break;
    }
    case 'clear': {
      saveLeads([]);
      console.log('✅ All leads cleared.');
      break;
    }
    default:
      console.log('Commands: add-lead, list, log <id> "note", export-csv, clear');
  }
}
