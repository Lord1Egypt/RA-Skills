/**
 * GitHub Bounty Scanner - Core Logic
 * Scans Algora and GitHub for high-value bounties with competition analysis
 */

const axios = require('axios');
const chalk = require('chalk');

class BountyScanner {
  constructor(options = {}) {
    this.githubToken = process.env.GITHUB_TOKEN;
    this.algoraApiKey = process.env.ALGORA_API_KEY;
    this.minBounty = options.minBounty || 100;
    this.maxCompetition = options.maxCompetition || 5;
    this.baseURL = 'https://api.github.com';
  }

  /**
   * Scan GitHub Issues with bounties
   */
  async scanGitHubIssues(query = 'bounty', limit = 50) {
    console.log(chalk.blue('🔍 Scanning GitHub for bounties...'));
    
    try {
      const response = await axios.get(`${this.baseURL}/search/issues`, {
        headers: {
          'Authorization': `token ${this.githubToken}`,
          'Accept': 'application/vnd.github.v3+json'
        },
        params: {
          q: `${query} is:issue is:open sort:created-desc`,
          per_page: limit
        }
      });

      const bounties = response.data.items.map(issue => ({
        id: issue.id,
        title: issue.title,
        url: issue.html_url,
        repo: issue.repository_url,
        createdAt: issue.created_at,
        updatedAt: issue.updated_at,
        comments: issue.comments,
        reactions: issue.reactions,
        labels: issue.labels.map(l => l.name),
        body: issue.body
      }));

      return this.filterAndScore(bounties);
    } catch (error) {
      console.error(chalk.red('❌ GitHub API Error:'), error.message);
      return [];
    }
  }

  /**
   * Scan Algora bounties
   */
  async scanAlgoraBounties(limit = 50) {
    console.log(chalk.blue('🔍 Scanning Algora for bounties...'));
    
    try {
      // Algora API endpoint (adjust based on actual API)
      const response = await axios.get('https://api.algora.io/v1/bounties', {
        headers: {
          'Authorization': `Bearer ${this.algoraApiKey}`
        },
        params: {
          status: 'open',
          limit: limit
        }
      });

      const bounties = response.data.map(bounty => ({
        id: bounty.id,
        title: bounty.title,
        url: bounty.url,
        repo: bounty.repository,
        bountyAmount: bounty.amount,
        currency: bounty.currency || 'USD',
        createdAt: bounty.created_at,
        deadline: bounty.deadline,
        skills: bounty.skills || [],
        difficulty: bounty.difficulty
      }));

      return this.filterAndScore(bounties);
    } catch (error) {
      console.error(chalk.red('❌ Algora API Error:'), error.message);
      return [];
    }
  }

  /**
   * Filter and score bounties based on competition and value
   */
  filterAndScore(bounties) {
    return bounties
      .filter(bounty => {
        // Filter by minimum bounty
        if (bounty.bountyAmount && bounty.bountyAmount < this.minBounty) {
          return false;
        }
        
        // Filter by competition (comments/PRs)
        const competition = bounty.comments || 0;
        if (competition > this.maxCompetition) {
          return false;
        }
        
        return true;
      })
      .map(bounty => ({
        ...bounty,
        score: this.calculateOpportunityScore(bounty),
        competitionLevel: this.getCompetitionLevel(bounty.comments || 0),
        recommendedAction: this.getRecommendedAction(bounty)
      }))
      .sort((a, b) => b.score - a.score);
  }

  /**
   * Calculate opportunity score (0-100)
   */
  calculateOpportunityScore(bounty) {
    let score = 50;

    // Bounty value scoring (0-30 points)
    if (bounty.bountyAmount) {
      if (bounty.bountyAmount >= 1000) score += 30;
      else if (bounty.bountyAmount >= 500) score += 20;
      else if (bounty.bountyAmount >= 200) score += 10;
    }

    // Competition scoring (0-40 points) - lower is better
    const comments = bounty.comments || 0;
    if (comments === 0) score += 40;
    else if (comments <= 2) score += 30;
    else if (comments <= 5) score += 20;
    else if (comments <= 10) score += 10;

    // Freshness scoring (0-20 points)
    const daysOld = this.getDaysOld(bounty.createdAt || bounty.created_at);
    if (daysOld <= 3) score += 20;
    else if (daysOld <= 7) score += 15;
    else if (daysOld <= 14) score += 10;
    else if (daysOld <= 30) score += 5;

    return Math.min(100, Math.max(0, score));
  }

  /**
   * Get competition level
   */
  getCompetitionLevel(comments) {
    if (comments === 0) return 'None';
    if (comments <= 2) return 'Low';
    if (comments <= 5) return 'Medium';
    if (comments <= 10) return 'High';
    return 'Very High';
  }

  /**
   * Get recommended action
   */
  getRecommendedAction(bounty) {
    const score = this.calculateOpportunityScore(bounty);
    
    if (score >= 80) return '🔥 HIGH PRIORITY - Apply immediately';
    if (score >= 60) return '✅ GOOD OPPORTUNITY - Consider applying';
    if (score >= 40) return '⚠️ MODERATE - Monitor for changes';
    return '❌ LOW PRIORITY - Skip or watch';
  }

  /**
   * Calculate days old from date string
   */
  getDaysOld(dateString) {
    if (!dateString) return 999;
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    return Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  }

  /**
   * Extract bounty amount from issue body
   */
  extractBountyAmount(body) {
    if (!body) return null;
    
    // Match patterns like "$500", "500 USD", "bounty: 1000"
    const patterns = [
      /\$([\d,]+)/,
      /(\d+)\s*USD/i,
      /bounty[:\s]+\$?([\d,]+)/i,
      /reward[:\s]+\$?([\d,]+)/i
    ];

    for (const pattern of patterns) {
      const match = body.match(pattern);
      if (match) {
        return parseInt(match[1].replace(',', ''));
      }
    }

    return null;
  }

  /**
   * Generate pricing recommendation
   */
  generatePricingRecommendation(bounties) {
    const avgBounty = bounties.reduce((sum, b) => sum + (b.bountyAmount || 0), 0) / bounties.length;
    const highValueCount = bounties.filter(b => (b.bountyAmount || 0) >= 500).length;
    const lowCompetitionCount = bounties.filter(b => (b.comments || 0) <= 2).length;

    let basePrice = 99;
    
    if (avgBounty > 500) basePrice = 149;
    if (avgBounty > 1000) basePrice = 199;
    if (highValueCount > 10) basePrice += 50;
    if (lowCompetitionCount > 20) basePrice += 30;

    return {
      recommendedPrice: basePrice,
      currency: 'USD',
      billingCycle: 'monthly',
      justification: `Based on ${bounties.length} bounties analyzed, average value $${avgBounty.toFixed(0)}, ${highValueCount} high-value opportunities`
    };
  }

  /**
   * Main scan function
   */
  async scan(options = {}) {
    const {
      github = true,
      algora = true,
      query = 'bounty',
      limit = 50,
      minBounty = 100,
      maxCompetition = 5
    } = options;

    this.minBounty = minBounty;
    this.maxCompetition = maxCompetition;

    let allBounties = [];

    if (github && this.githubToken) {
      const githubBounties = await this.scanGitHubIssues(query, limit);
      allBounties = [...allBounties, ...githubBounties];
    }

    if (algora && this.algoraApiKey) {
      const algoraBounties = await this.scanAlgoraBounties(limit);
      allBounties = [...allBounties, ...algoraBounties];
    }

    // Remove duplicates and sort by score
    const uniqueBounties = allBounties.filter(
      (v, i, a) => a.findIndex(t => t.url === v.url) === i
    );

    const pricingRec = this.generatePricingRecommendation(uniqueBounties);

    return {
      bounties: uniqueBounties,
      totalFound: uniqueBounties.length,
      highPriority: uniqueBounties.filter(b => b.score >= 80).length,
      goodOpportunities: uniqueBounties.filter(b => b.score >= 60 && b.score < 80).length,
      pricingRecommendation: pricingRec,
      scannedAt: new Date().toISOString()
    };
  }
}

module.exports = BountyScanner;
