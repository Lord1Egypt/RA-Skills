const path = require('path');
const refs = require('./references.json');

/**
 * Mad SEO Content Version 1.0 (Lean 11-Tool Architecture)
 * The ultimate autonomous SEO/GEO engine for blog growth and topical authority.
 * Highly optimized for OpenClaw context efficiency and autonomous execution.
 */

exports.tools = {
  /**
   * Provides an interactive V6 onboarding dashboard for the user.
   */
  async onboard() {
    return {
      success: true,
      instructions: `Run the MAD SEO CONTENT 1.2.0 ONBOARDING Workflow:
      1. **Introduction**: Introduce yourself as the Omnichannel SEO Director (Universal WP Edition).
      2. **Dependency Check**: Verify 'scrapling-official', 'api-gateway', and 'agent-browser'.
      3. **Data Collection**: Ask the user for the following configuration:
         - **Target Language** (e.g., "it" for Italian, "en" for English).
         - **Brand Name & Core Service**.
         - **Output Format**: "html" (preferred for WP) or "markdown".
         - **WordPress Config**: URL, User, and Application Password.
         - **SEO Plugin**: "rank_math", "yoast", or "none".
           *IMPORTANT*: If using Rank Math, inform the user they MUST install 'Rank Math API Manager' from GitHub: https://github.com/Devora-AS/rank-math-api-manager
         - **WP Categories**: A mapping of IDs to names (e.g., {5: "Guide", 10: "SEO"}).
         - **Publication Days**: e.g., ["mon", "wed", "sat"].
      4. **State Initialization**: Save to './shared/mad_seo/PROJECT_STRATEGY.json' and init the SQLite DB.
      5. **Security & Trust Model**: 
         - Explicitly inform the user that WordPress credentials will be stored in a sub-folder of the shared workspace.
         - **Transparency**: Disclose that 'api-gateway' handles GSC/GA4, while 'agent-browser' and 'scrapling' perform outbound network requests to public SEO/Social endpoints. No telemetry or secondary storage is used.
         - **Recommendation**: Advise the user to only run this skill alongside trusted, verified dependencies.`,
    };
  },

  /**
   * Performs Omnichannel 3.0 strategic research with Social Discovery.
   */
  async research_strategy({ topic }) {
    return {
      success: true,
      instructions: `Conduct an Omnichannel strategic analysis for "${topic}".
      1. **Internal Context**: Query existing posts from WordPress (or the local ENTITY_MAP.json) to see what has already been covered on this topic.
      2. **Language Focus**: Use the configured 'language' parameter.
      3. **SERP Intelligence**: Identify Skyscraper 3.0 content gaps in the Top 10.
      4. **Social Discovery**: Use 'scrapling' to analyze platforms for real-world pain points.`,
      reference: refs.engine_strategy,
      local_benchmarks: refs.local_compliance
    };
  },

  /**
   * Generates a 12-month strategy AND creates the monthly SQLite editorial calendar.
   */
  async plan_strategy({ niche, location }) {
    return {
      success: true,
      instructions: `Execute the Full-Year Strategy Planning Protocol for [${niche}] in [${location}]:
      1. **Inventory Audit**: Fetch existing post titles/slugs from WordPress to prevent duplicates.
      2. **12-Month Calendar**: Generate a complete editorial calendar for the next 52 weeks (respecting 'publication_days').
      3. **Strategic Variety**: Ensure a balanced mix of TOFU/MOFU/BOFU, mapping each stage to the user's specific WordPress Categories (e.g., TOFU -> "Guide").
      4. **WP Category Mapping**: Assign every single planned post to the correct 'wp_category_id' based on the stage mapping.
      5. **SQL Batch Insert**: Insert all ~150+ planned titles and dates into the SQLite 'content_calendar' table.`,
      roadmap_logic: refs.roadmap_strategy,
      funnel_strategy: refs.funnel_strategy,
      db_schema: refs.db_schema
    };
  },

  /**
   * Generates GEO-optimized content, applies the Human-GEO pass natively, and outputs headlines.
   */
  async draft_article({ topic, target_keyword }) {
    const configPath = './references/humanizer_config.json';
    return {
      success: true,
      instructions: `Draft, Humanize, and Title the article for "${topic}" targeting "${target_keyword}".
      1. **Output Format**: Generate content in the configured 'output_format' (HTML or Markdown). If HTML, use semantic tags (h2, p, figure, etc.).
      2. **Language**: Use the configured 'language' for all text generation.
      3. **Writing**: Draft a 1,500-3,000 word pillar post.
      4. **Humanization Pass**: Natively apply the Human-GEO Framework (referenced in '${configPath}').
      5. **Output**: Write the final draft to './shared/mad_seo/content/[topic].[ext]'.`,
      quality_standards: refs.writer_quality,
      structure_templates: refs.structure_templates,
      title_library: refs.title_formulas,
      humanizer_config: configPath
    };
  },

  /**
   * Comprehensive EEAT Audit: Checks the article for fabrication AND the author's bio.
   */
  async audit_eeat({ file_path, author_bio }) {
    return {
      success: true,
      instructions: `Perform a Unified Content 1.0 EEAT Audit of ${file_path} and the provided Author Bio.
      1. **Fabrication Check**: Scan the article for "I remember when..." or subjective claims not backed by data.
      2. **Information Gain**: Verify the article contains at least 3 unique concepts not found in the SERP Top 10.
      3. **Author Authority**: Evaluate the 'author_bio'. Suggest improvements to secure higher "Expertise" markers.
      4. **Output**: Generate a single EEAT Score (0-100) combining Content Trust and Author Trust.`,
      eeat_benchmarks: refs.writer_quality
    };
  },

  /**
   * Generates GEO-optimized JSON-LD schema blocks.
   */
  async generate_schema({ content_path, type }) {
    return {
      success: true,
      instructions: `Analyze ${content_path} and generate a Content 1.0 GEO-Optimized "${type}" Schema.
      1. **SEO Plugin Integration**: If a plugin (Rank Math/Yoast) is configured, prepare the API payload for the respective meta update endpoint instead of just JSON-LD.
      2. **Entity Grounding**: Inject Knowledge Graph IDs (Wikidata) where applicable.`,
      schema_logic: refs.schema_architect
    };
  },

  /**
   * Performs an autonomous Site-Wide Deep Intelligence and Entity Mapping.
   */
  async site_wide_intelligence({ sitemap_url, gsc_property }) {
    return {
      success: true,
      instructions: `Run a Content 1.0 GLOBAL SITE INTELLIGENCE AUDIT for: ${sitemap_url}.
      1. **Global Entity Map**: Build the entity map file containing all site entities and their relationships.
      2. **GSC Correlation**: Correlate sitemap URLs with GSC performance metrics.
      3. **Master Prescription**: Write individualized optimization reports to the 'audits' folder in the './shared/mad_seo/' directory.`,
      audit_standards: refs.writer_quality
    };
  },

  /**
   * Automatically finds older, high-authority posts and injects contextual links to a newly published post.
   */
  async inject_internal_links({ new_post_path, new_post_topic, dry_run = false }) {
    return {
      success: true,
      instructions: `Run the Content 1.0 Internal Link Injection sequence for "${new_post_topic}":
      1. **Analysis**: Use './shared/mad_seo/ENTITY_MAP.json' to find 3 semantically related, existing high-authority posts.
      2. **Drafting**: Prepare the new contextual sentences for each post.
      3. **Review**: Present the proposed changes (Diff) to the user.
      4. **Safety Verification**: 
         - If 'dry_run' is true, ONLY output the proposed changes. Do not edit files.
         - If 'dry_run' is false, you MUST wait for explicit user confirmation of the diff before writing to the markdown files.`
    };
  },

  /**
   * Slices a pillar post into multiple distribution formats for omnichannel marketing.
   */
  async repurpose_content({ file_path }) {
    return {
      success: true,
      instructions: `Analyze ${file_path} and execute the 'One-to-Many' repurposing protocol:
      1. **Twitter/X**: Extract 3 core insights to create an engaging Thread.
      2. **LinkedIn**: Rewrite the introduction into a high-authority narrative post.
      3. **Newsletter**: Draft a 150-word teaser linking to the main article.
      4. Save outputs to './shared/mad_seo/distribution/' and update the SQLite 'content_calendar' status to 'Repurposed'.`,
      funnel_strategy: refs.funnel_strategy
    };
  },

  /**
   * Analyzes AI search responses to calculate AI Citation Share.
   */
  async analyze_share_of_voice({ domain, topics }) {
    return {
      success: true,
      instructions: `Perform a general AI Citation Share analysis for ${domain} across [${topics.join(', ')}].
      1. **AI Scrape**: Use 'agent-browser' to query Gemini and Perplexity for these topics.
      2. **Citation Extract**: Identify which domains are currently being cited as primary sources.
      3. **Score Calculation**: Calculate the "Share of AI Voice" percentage for ${domain}.
      4. **Gap Analysis**: If ${domain} is missing, identify the specific "Relationship Facts" being cited from competitors.`,
    };
  },

  /**
   * Unified Analytics Suite (Handles Performance, Decay, and Cannibalization).
   */
  async analytics_suite({ audit_type, site_url, target_keyword }) {
    return {
      success: true,
      instructions: `Run the Analytics Suite via 'api-gateway' for audit type: [${audit_type}].
      1. **If 'low_ctr'**: Fetch GSC data to find "High Impression / Low CTR" optimization targets and recommend title/schema changes.
      2. **If 'decay'**: Identify URLs where traffic dropped >20% YoY. Mark them in the SQLite 'content_calendar' for a 'Refresh'.
      3. **If 'cannibalization'**: Check if multiple URLs receive impressions for "${target_keyword}". Suggest 301 redirects or canonical tags for the loser.`
    };
  },
  /**
   * Creates a WordPress draft via REST API, uploads media, and sets SEO meta.
   */
  async create_wp_draft({ title, content_file, category_id, featured_image_path }) {
    return {
      success: true,
      instructions: `Execute the WordPress Publishing Protocol for "${title}":
      1. **Media Upload**: Upload the image from '${featured_image_path}' to the WP Media Library and capture the 'attachment_id'.
      2. **Post Creation**: Create a new 'draft' post with the HTML content from '${content_file}', assigned to category ID ${category_id}.
      3. **SEO Meta Update**: 
         - If **Rank Math**: Send meta update to '/wp-json/rank-math-api/v1/update-meta'.
         - If **Yoast**: Update meta fields via the standard REST API post update.
      4. **Verification**: Confirm the post ID and provide the preview URL.`,
      wp_auth_logic: "Basic Auth (User + Application Password)",
      rest_endpoints: {
        posts: "/wp-json/wp/v2/posts",
        media: "/wp-json/wp/v2/media",
        rank_math: "/wp-json/rank-math-api/v1/update-meta"
      }
    };
  }
};

// OpenClaw Mad SEO Content 1.0 Argument Decorators
exports.onboard.args = {};
exports.research_strategy.args = { topic: 'string' };
exports.plan_strategy.args = { niche: 'string', location: 'string' };
exports.draft_article.args = { topic: 'string', target_keyword: 'string' };
exports.audit_eeat.args = { file_path: 'string', author_bio: 'string?' };
exports.generate_schema.args = { content_path: 'string', type: 'string' };
exports.site_wide_intelligence.args = { sitemap_url: 'string', gsc_property: 'string' };
exports.inject_internal_links.args = { new_post_path: 'string', new_post_topic: 'string', dry_run: 'boolean?' };
exports.repurpose_content.args = { file_path: 'string' };
exports.analyze_share_of_voice.args = { domain: 'string', topics: 'string[]' };
exports.analytics_suite.args = { audit_type: 'string', site_url: 'string', target_keyword: 'string?' };
exports.create_wp_draft.args = { title: 'string', content_file: 'string', category_id: 'number', featured_image_path: 'string' };
