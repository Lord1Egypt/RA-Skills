const nodemailer = require('nodemailer');

/**
 * Email Notifier
 */
class EmailNotifier {
  constructor(config) {
    this.config = config;
    this.transporter = null;

    if (config.host && config.user && config.pass) {
      this.transporter = nodemailer.createTransport({
        host: config.host,
        port: config.port || 587,
        secure: false,
        auth: {
          user: config.user,
          pass: config.pass
        }
      });
    }
  }

  /**
   * Send trending report via email
   * @param {string} to - Recipient email
   * @param {Array} repos - Trending repositories
   * @param {object} options - Additional options
   */
  async sendTrendingReport(to, repos, options = {}) {
    if (!this.transporter) {
      console.warn('Email transporter not configured');
      return false;
    }

    const html = this.createHTML(repos, options);
    const { language = 'All', since = 'daily' } = options;
    const timeLabel = { daily: 'Today', weekly: 'This Week', monthly: 'This Month' }[since] || 'Today';

    try {
      await this.transporter.sendMail({
        from: `"GitHub Trending Monitor" <${this.config.user}>`,
        to,
        subject: `🔥 GitHub Trending - ${timeLabel} (${language})`,
        html
      });
      return true;
    } catch (error) {
      console.error('Email send failed:', error.message);
      return false;
    }
  }

  /**
   * Create HTML email content
   */
  createHTML(repos, options = {}) {
    const { language = 'All', since = 'daily' } = options;
    const timeLabel = { daily: 'Today', weekly: 'This Week', monthly: 'This Month' }[since] || 'Today';

    let html = `
      <!DOCTYPE html>
      <html>
      <head>
        <meta charset="UTF-8">
        <style>
          body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #24292e; }
          .container { max-width: 800px; margin: 0 auto; padding: 20px; }
          .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 10px; }
          .header h1 { margin: 0; font-size: 28px; }
          .header p { margin: 10px 0 0 0; opacity: 0.9; }
          .repo { background: #f6f8fa; padding: 20px; margin: 20px 0; border-left: 4px solid #0366d6; border-radius: 6px; }
          .repo-title { font-size: 20px; font-weight: 600; color: #0366d6; margin-bottom: 10px; }
          .repo-title a { color: #0366d6; text-decoration: none; }
          .repo-title a:hover { text-decoration: underline; }
          .repo-desc { color: #586069; margin: 10px 0; }
          .repo-stats { display: flex; gap: 20px; margin-top: 10px; }
          .stat { display: flex; align-items: center; gap: 5px; color: #586069; }
          .stat-value { font-weight: 600; color: #24292e; }
          .footer { text-align: center; padding: 20px; color: #586069; font-size: 14px; margin-top: 30px; border-top: 1px solid #e1e4e8; }
        </style>
      </head>
      <body>
        <div class="container">
          <div class="header">
            <h1>🔥 GitHub Trending - ${timeLabel}</h1>
            <p>${language && language !== 'all' ? `Language: ${language}` : 'All Languages'}</p>
            <p>${new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' })}</p>
          </div>
    `;

    if (!repos || repos.length === 0) {
      html += '<div class="repo"><p>❌ No trending repositories found.</p></div>';
    } else {
      repos.slice(0, 10).forEach((repo, index) => {
        html += `
          <div class="repo">
            <div class="repo-title">
              ${index + 1}. <a href="${repo.url}" target="_blank">${repo.fullName}</a>
            </div>
            <div class="repo-desc">${repo.description || 'No description provided.'}</div>
            <div class="repo-stats">
              <div class="stat">⭐ <span class="stat-value">${repo.stars.toLocaleString()}</span> stars</div>
              <div class="stat">🍴 <span class="stat-value">${repo.forks.toLocaleString()}</span> forks</div>
              ${repo.todayStars > 0 ? `<div class="stat">📈 <span class="stat-value">+${repo.todayStars}</span> today</div>` : ''}
              ${repo.language ? `<div class="stat">💻 <span class="stat-value">${repo.language}</span></div>` : ''}
            </div>
          </div>
        `;
      });
    }

    html += `
          <div class="footer">
            <p>💡 Powered by GitHub Trending Monitor</p>
            <p>⚡ Subscribe for daily updates!</p>
          </div>
        </div>
      </body>
      </html>
    `;

    return html;
  }
}

module.exports = EmailNotifier;
