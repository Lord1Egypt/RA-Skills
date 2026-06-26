---
name: google-analytics-intelligence
description: "Analyze GA4 data, detect traffic anomalies, and generate actionable growth recommendations. Use when the user needs revenue tracking, anomaly detection, or traffic optimization insights."
version: 1.0.0
homepage: https://github.com/ncreighton/empire-skills
metadata:
  {
    "openclaw": {
      "requires": {
        "env": ["GOOGLE_ANALYTICS_PROPERTY_ID", "GOOGLE_ANALYTICS_API_KEY", "SLACK_WEBHOOK_URL"],
        "bins": ["python3", "curl"]
      },
      "os": ["macos", "linux", "win32"],
      "files": ["SKILL.md"],
      "emoji": "📊"
    }
  }
---

## Overview

**Google Analytics Intelligence** is a comprehensive revenue tracking and growth optimization skill that transforms raw GA4 data into actionable business intelligence. This skill automatically pulls real-time analytics from your Google Analytics 4 property, applies statistical anomaly detection to identify unusual traffic patterns, generates professional reports, and suggests data-driven growth actions.

### Why This Matters

Modern businesses generate massive amounts of analytics data but lack the time to analyze it deeply. This skill bridges that gap by:

- **Automating data extraction** from GA4 via the Google Analytics Data API
- **Detecting anomalies** using statistical methods (standard deviation, trend analysis)
- **Generating professional reports** with visualizations and insights
- **Suggesting growth actions** based on traffic patterns and conversion data
- **Integrating with Slack** for real-time alerts on significant changes
- **Supporting WordPress, Shopify, and custom web properties** through GA4 universal tracking

Perfect for marketing teams, SaaS founders, e-commerce managers, and growth analysts who need intelligence without manual dashboard analysis.

---

## Quick Start

Try these prompts immediately to see the skill in action:

### Example 1: Weekly Analytics Summary
```
Analyze my GA4 data for the last 7 days and generate a comprehensive 
report showing page views, users, bounce rate, and conversion metrics. 
Include a comparison to the previous week and flag any significant changes.
```

### Example 2: Anomaly Detection Alert
```
Check my GA4 traffic for the last 30 days and identify any unusual patterns 
or spikes. Tell me which pages or traffic sources show anomalies, and suggest 
what might have caused them.
```

### Example 3: Growth Recommendations
```
Based on my GA4 data, what are my top 5 performing pages by engagement? 
Generate 3 specific growth actions I could take to increase traffic to 
underperforming pages.
```

### Example 4: Revenue Tracking Deep Dive
```
Pull conversion and revenue data from GA4 for Q4 2024. Show me conversion 
rates by traffic source, average order value by device type, and identify 
which channels drive the most revenue per visitor.
```

### Example 5: Real-Time Dashboard Export
```
Create a Slack-ready summary of today's GA4 performance metrics including 
active users, top pages, bounce rate, and conversion funnel status. Alert 
me if anything is outside normal ranges.
```

---

## Capabilities

### 1. **Real-Time Data Extraction**
Connects directly to Google Analytics 4 via the official Google Analytics Data API (v1beta). Pulls:
- User metrics (active users, new users, returning users, user engagement)
- Page/screen metrics (page views, scroll depth, time on page)
- Traffic source data (organic, direct, referral, paid, social)
- Conversion metrics (transactions, revenue, goal completions)
- Device and demographic breakdowns
- Custom event tracking data

**Usage Example:**
```
Pull all conversion events from my GA4 property for the last 30 days, 
broken down by traffic source and device type. Include revenue data.
```

### 2. **Statistical Anomaly Detection**
Applies multiple detection methods:
- **Z-score analysis** (identifies values >2 standard deviations from mean)
- **Trend detection** (compares week-over-week and month-over-month changes)
- **Seasonal adjustment** (accounts for day-of-week and seasonal patterns)
- **Threshold-based alerts** (custom rules for your business metrics)

Flags anomalies with severity levels (minor, moderate, critical).

**Usage Example:**
```
Run anomaly detection on my bounce rate for the last 90 days. 
Show me which days had unusual patterns and what the normal range is.
```

### 3. **Professional Report Generation**
Creates publication-ready reports including:
- Executive summary with key metrics and insights
- Trend visualizations (line charts, bar charts)
- Comparison tables (current vs. previous period)
- Anomaly highlights with context
- Conversion funnel analysis
- Traffic source attribution
- Device and user behavior breakdowns
- Export to PDF, HTML, or Markdown

**Usage Example:**
```
Generate a professional monthly report for January 2025 showing all key 
metrics, anomalies, and trends. Format it for sharing with stakeholders.
```

### 4. **Growth Recommendations Engine**
AI-powered suggestions based on:
- Identifying high-engagement pages and replicating their characteristics
- Spotting underperforming content and optimization opportunities
- Analyzing traffic source efficiency and budget allocation
- Detecting conversion bottlenecks in user funnels
- Recommending content topics based on search traffic patterns
- Suggesting A/B test ideas based on performance gaps

**Usage Example:**
```
Analyze my top 10 pages by engagement. What do they have in common? 
Suggest 5 specific changes I could make to my lowest-performing pages 
to increase engagement.
```

### 5. **Slack Integration**
Sends automated alerts and summaries:
- Daily/weekly digest reports
- Real-time anomaly alerts (when significant changes occur)
- Conversion milestone notifications
- Traffic source performance summaries
- Custom metric monitoring

**Usage Example:**
```
Set up a daily Slack alert that sends me a summary of yesterday's GA4 
metrics every morning at 8 AM, with alerts if bounce rate exceeds 60% 
or conversions drop below 5.
```

### 6. **Multi-Property Support**
Works with:
- Standard GA4 web properties
- WordPress sites with GA4 tracking
- Shopify stores with GA4 integration
- Mobile apps with GA4 Firebase integration
- Custom event implementations

---

## Configuration

### Required Environment Variables

Set these in your environment or `.env` file:

```bash
# Google Analytics Configuration
GOOGLE_ANALYTICS_PROPERTY_ID=123456789          # Your GA4 Property ID (numeric)
GOOGLE_ANALYTICS_API_KEY=AIzaSy...              # Google Cloud API Key with GA4 access
GOOGLE_ANALYTICS_VIEW_ID=ga4:123456789          # GA4 view identifier

# Optional: Service Account for advanced access
GOOGLE_SERVICE_ACCOUNT_JSON=/path/to/service-account.json

# Slack Integration (optional)
SLACK_WEBHOOK_URL=https://hooks.slack.com/...   # For alert notifications
SLACK_CHANNEL=#analytics                        # Default channel

# Configuration Options
ANOMALY_SENSITIVITY=2.0                         # Z-score threshold (1.5-3.0)
REPORT_TIMEZONE=America/New_York                # Your timezone
CURRENCY=USD                                    # For revenue metrics
```

### Setup Instructions

#### Step 1: Enable Google Analytics API
1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Create a new project or select existing
3. Enable "Google Analytics Data API" (v1beta)
4. Create an API key (Credentials → Create Credentials → API Key)
5. Copy the API key to `GOOGLE_ANALYTICS_API_KEY`

#### Step 2: Get Your Property ID
1. Log into [Google Analytics 4](https://analytics.google.com)
2. Go to Admin → Property Settings
3. Copy your Property ID (numeric value)
4. Set `GOOGLE_ANALYTICS_PROPERTY_ID`

#### Step 3: Optional - Slack Integration
1. Create a Slack App at [api.slack.com](https://api.slack.com)
2. Enable Incoming Webhooks
3. Create a webhook for your target channel
4. Copy webhook URL to `SLACK_WEBHOOK_URL`

#### Step 4: Verify Connection
```
Test the GA4 connection by running a simple query to fetch 
yesterday's page views. The skill will confirm API access is working.
```

---

## Example Outputs

### Output 1: Weekly Analytics Report

```
GOOGLE ANALYTICS WEEKLY REPORT
Week of Jan 20-26, 2025
================================

KEY METRICS
-----------
Total Users:           12,847 (↑ 8.3% vs previous week)
New Users:             3,421 (↑ 12.1%)
Sessions:              18,934 (↑ 6.2%)
Pageviews:             67,234 (↑ 5.8%)
Avg Session Duration:  2m 34s (↓ 0.5%)
Bounce Rate:           42.3% (↑ 1.2%)
Conversion Rate:       3.2% (↑ 0.4%)
Total Revenue:         $18,450 (↑ 15.2%)

TOP PAGES (by pageviews)
------------------------
1. /pricing                    8,234 views (12.2% of total)
2. /features                   7,856 views (11.7%)
3. /blog/seo-guide-2025        6,421 views (9.5%)
4. /                           5,987 views (8.9%)
5. /case-studies               4,234 views (6.3%)

TRAFFIC SOURCES
---------------
Organic Search:   45.2% (7,234 users, $12,340 revenue)
Direct:          28.1% (4,567 users, $4,230 revenue)
Referral:        15.3% (2,345 users, $1,567 revenue)
Social:           8.2% (1,234 users, $456 revenue)
Paid Search:      3.2% (467 users, $-1,143 cost)

ANOMALIES DETECTED
------------------
⚠️  MODERATE: Bounce rate on /blog increased to 68% (normal: 45%)
   Possible cause: Recent traffic spike from Reddit
   
🔴 CRITICAL: Conversion rate dropped 22% on /checkout on Jan 24
   Possible cause: Payment gateway timeout issues
   Action: Check payment provider logs immediately

GROWTH RECOMMENDATIONS
----------------------
1. Replicate /pricing page design on /features (12% higher engagement)
2. Create 3 more blog posts in "SEO" category (top performer)
3. Increase organic traffic investment (highest ROI at $1.70 per user)
4. A/B test CTA button color on /pricing (current: 2.8% conversion)
5. Reduce paid search spend (negative ROI, $2.45 cost per conversion)
```

### Output 2: Anomaly Detection Alert

```
🚨 ANOMALY DETECTION ALERT
Time: Jan 27, 2025 - 2:34 PM
================================

CRITICAL ANOMALIES
-------------------
1. Traffic Spike on /product-launch page
   Current: 4,234 pageviews (vs. avg 234)
   Severity: CRITICAL (Z-score: 18.2)
   Likely Cause: Product hunt launch or press coverage
   Recommendation: Monitor conversion rate, ensure server capacity

2. Bounce Rate Increase (Overall)
   Current: 48.2% (vs. avg 42.1%)
   Severity: MODERATE (Z-score: 2.3)
   Affected Pages: /blog (68%), /resources (55%)
   Recommendation: Check page load times, review recent content changes

POSITIVE ANOMALIES
-------------------
✅ Conversion Rate Spike
   Current: 4.1% (vs. avg 3.2%)
   Severity: POSITIVE
   Likely Cause: New landing page variant performing well
   Recommendation: Continue monitoring, consider rolling out to all traffic

NORMAL RANGES (Last 30 Days)
----------------------------
Metric                  Min    Avg    Max    Current  Status
Users/Day              234    567    892    612      ✅ Normal
Sessions/Day           345    834   1,234   876      ✅ Normal
Bounce Rate            38%    42%    48%    48.2%    ⚠️  High
Conversion Rate       2.1%   3.2%   4.5%    4.1%    ✅ Good
Avg Session Duration  1m45s  2m34s  3m12s  2m41s    ✅ Normal
```

### Output 3: Growth Recommendations

```
📈 GROWTH RECOMMENDATIONS
Based on GA4 Analysis (Last 90 Days)
================================

QUICK WINS (Implement This Week)
---------------------------------
1. Replicate /pricing page design on /features
   Impact: +12% engagement, +0.8% conversion
   Effort: Medium (2-3 days)
   Estimated Revenue Lift: +$2,400/month

2. Expand "SEO Guides" blog category
   Current: 3 posts generating 18K pageviews
   Recommendation: Create 5 more posts in this series
   Estimated Impact: +45K pageviews/month, +$3,200 revenue

3. Optimize /checkout funnel
   Current: 22% drop-off at payment step
   Recommendation: A/B test guest checkout, reduce form fields
   Estimated Impact: +1.4% conversion rate = +$4,100/month

MEDIUM-TERM INITIATIVES (30-90 Days)
-------------------------------------
4. Paid Search Optimization
   Current ROI: -$0.45 per user
   Recommendation: Pause underperforming campaigns, reallocate budget
   Potential Savings: +$2,100/month

5. Content Repurposing Strategy
   Top Pages: /pricing (8.2K views), /features (7.9K views)
   Recommendation: Create video, infographic, and email versions
   Estimated Impact: +25% engagement, reach new audiences

STRATEGIC OPPORTUNITIES (90+ Days)
-----------------------------------
6. Organic Search Dominance
   Current: 45.2% of traffic, highest ROI ($1.70/user)
   Recommendation: Implement comprehensive SEO strategy
   Target: Increase organic to 60% of traffic
   Projected Revenue: +$8,400/month

7. Email Nurture Sequence
   Opportunity: 28.1% direct traffic suggests repeat visitors
   Recommendation: Build email list, create nurture sequence
   Projected Conversion Lift: +0.6% = +$2,800/month

ESTIMATED COMBINED IMPACT
--------------------------
Quick Wins:         +$9,700/month
Medium-term:        +$2,100/month
Strategic:          +$11,200/month
Total Potential:    +$23,000/month revenue increase
```

---

## Tips & Best Practices

### 1. **Set Up Baseline Metrics First**
Before relying on anomaly detection, run the skill for 30 days to establish normal ranges. This improves accuracy of anomaly flagging.

```
Run a 30-day baseline analysis to understand my normal traffic patterns, 
conversion rates, and seasonal variations before enabling alerts.
```

### 2. **Use Segmentation for Deeper Insights**
Don't just look at overall metrics—segment by traffic source, device, or user type to find hidden patterns.

```
Compare conversion rates across all traffic sources. Which source converts 
best? Which needs optimization? Show me the funnel for each.
```

### 3. **Combine with Other Data Sources**
Correlate GA4 data with your CRM, email platform, or ad spend data for complete picture.

```
I'll provide my ad spend data from Facebook Ads Manager. Cross-reference 
it with GA4 to calculate true ROI by campaign.
```

### 4. **Create Custom Events for Your Business**
GA4's event tracking is powerful. Define custom events that matter to your business (sign-ups, demo requests, etc.).

```
Set up custom events in GA4 for: free trial signups, demo requests, 
and pricing page interactions. Then analyze their impact on revenue.
```

### 5. **Schedule Regular Reports**
Set up weekly or monthly automated reports to Slack or email. This keeps stakeholders informed without manual work.

```
Generate a weekly report every Monday at 9 AM and send it to my Slack 
#analytics channel. Include last week's performance vs. previous week.
```

### 6. **Monitor Seasonality**
Adjust your expectations based on seasons. E-commerce sites see spikes in Nov-Dec, SaaS sees slower summers.