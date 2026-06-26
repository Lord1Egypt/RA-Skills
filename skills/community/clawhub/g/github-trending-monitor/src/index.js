require('dotenv').config();
const express = require('express');
const SkillPayment = require('./payment');
const GitHubTrendingScraper = require('./scrapers/github');
const TelegramNotifier = require('./notifiers/telegram');
const DiscordNotifier = require('./notifiers/discord');
const EmailNotifier = require('./notifiers/email');
const Scheduler = require('./scheduler');

/**
 * GitHub Trending Monitor Application
 */
class GitHubTrendingMonitor {
  constructor() {
    this.app = express();
    this.port = process.env.PORT || 3000;

    // Initialize payment system
    this.payment = new SkillPayment(process.env.SKILLPAY_API_KEY);

    // Initialize scraper
    this.scraper = new GitHubTrendingScraper(process.env.GITHUB_TOKEN);

    // Initialize notifiers
    this.telegramNotifier = new TelegramNotifier(process.env.TELEGRAM_BOT_TOKEN);
    this.discordNotifier = new DiscordNotifier(process.env.DISCORD_WEBHOOK_URL);
    this.emailNotifier = new EmailNotifier({
      host: process.env.EMAIL_HOST,
      port: process.env.EMAIL_PORT,
      user: process.env.EMAIL_USER,
      pass: process.env.EMAIL_PASS
    });

    // Initialize scheduler
    this.scheduler = new Scheduler();

    // Subscription storage (use database in production)
    this.subscriptions = new Map();

    this.setupMiddleware();
    this.setupRoutes();
    this.setupScheduledTasks();
  }

  /**
   * Setup Express middleware
   */
  setupMiddleware() {
    this.app.use(express.json());
    this.app.use(express.urlencoded({ extended: true }));

    // CORS
    this.app.use((req, res, next) => {
      res.header('Access-Control-Allow-Origin', '*');
      res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization');
      next();
    });

    // Logging
    this.app.use((req, res, next) => {
      console.log(`[${new Date().toISOString()}] ${req.method} ${req.path}`);
      next();
    });
  }

  /**
   * Setup API routes
   */
  setupRoutes() {
    // Health check
    this.app.get('/health', (req, res) => {
      res.json({ status: 'ok', timestamp: new Date().toISOString() });
    });

    // Get trending repositories
    this.app.get('/trending', async (req, res) => {
      try {
        const { language = '', since = 'daily' } = req.query;

        const repos = await this.scraper.getTrending(language, since);

        res.json({
          success: true,
          data: repos,
          count: repos.length,
          language: language || 'all',
          since
        });
      } catch (error) {
        console.error('Trending endpoint error:', error);
        res.status(500).json({ error: error.message });
      }
    });

    // Trigger notification
    this.app.post('/notify', async (req, res) => {
      try {
        const { userId, transactionId, channels, language = '', since = 'daily' } = req.body;

        // Verify payment
        const paymentVerified = await this.payment.verifyPayment(userId, transactionId);
        if (!paymentVerified) {
          return res.status(402).json({ error: 'Payment required or verification failed' });
        }

        // Fetch trending repos
        const repos = await this.scraper.getTrending(language, since);

        // Send notifications
        const results = await this.sendNotifications(repos, channels, { language, since });

        // Log usage
        await this.payment.logUsage(userId, 'notify');

        res.json({
          success: true,
          data: {
            repoCount: repos.length,
            notifications: results
          }
        });
      } catch (error) {
        console.error('Notify endpoint error:', error);
        res.status(500).json({ error: error.message });
      }
    });

    // Subscribe to daily notifications
    this.app.post('/subscribe', async (req, res) => {
      try {
        const { userId, channels, preferences = {} } = req.body;

        if (!userId || !channels) {
          return res.status(400).json({ error: 'Missing required fields: userId, channels' });
        }

        // Create payment request
        const paymentRequest = await this.payment.createPaymentRequest(userId);

        // Save subscription (pending payment)
        this.subscriptions.set(userId, {
          channels,
          preferences: {
            language: preferences.language || '',
            since: preferences.since || 'daily',
            schedule: preferences.schedule || process.env.SCHEDULE || '0 9 * * *'
          },
          status: 'pending',
          paymentId: paymentRequest.paymentId,
          createdAt: new Date().toISOString()
        });

        res.json({
          success: true,
          message: 'Subscription created, please complete payment',
          payment: paymentRequest
        });
      } catch (error) {
        console.error('Subscribe endpoint error:', error);
        res.status(500).json({ error: error.message });
      }
    });

    // Unsubscribe
    this.app.post('/unsubscribe', async (req, res) => {
      try {
        const { userId } = req.body;

        if (!userId) {
          return res.status(400).json({ error: 'Missing userId' });
        }

        this.subscriptions.delete(userId);

        res.json({
          success: true,
          message: 'Subscription cancelled'
        });
      } catch (error) {
        console.error('Unsubscribe endpoint error:', error);
        res.status(500).json({ error: error.message });
      }
    });

    // Get subscription status
    this.app.get('/subscription/:userId', (req, res) => {
      const { userId } = req.params;
      const subscription = this.subscriptions.get(userId);

      if (!subscription) {
        return res.status(404).json({ error: 'Subscription not found' });
      }

      res.json({
        success: true,
        subscription
      });
    });

    // Payment callback
    this.app.post('/payment/callback', async (req, res) => {
      try {
        const { userId, paymentId, status } = req.body;

        if (status === 'completed') {
          const subscription = this.subscriptions.get(userId);
          if (subscription && subscription.paymentId === paymentId) {
            subscription.status = 'active';
            this.subscriptions.set(userId, subscription);
          }
        }

        res.json({ success: true });
      } catch (error) {
        console.error('Payment callback error:', error);
        res.status(500).json({ error: error.message });
      }
    });
  }

  /**
   * Send notifications to multiple channels
   */
  async sendNotifications(repos, channels = {}, options = {}) {
    const results = {};

    // Telegram
    if (channels.telegram && channels.telegram.chatId) {
      results.telegram = await this.telegramNotifier.sendTrendingReport(
        channels.telegram.chatId,
        repos,
        options
      );
    }

    // Discord
    if (channels.discord) {
      results.discord = await this.discordNotifier.sendTrendingReport(repos, options);
    }

    // Email
    if (channels.email && channels.email.to) {
      results.email = await this.emailNotifier.sendTrendingReport(
        channels.email.to,
        repos,
        options
      );
    }

    return results;
  }

  /**
   * Setup scheduled tasks
   */
  setupScheduledTasks() {
    const schedule = process.env.SCHEDULE || '0 9 * * *';

    this.scheduler.addTask(
      schedule,
      async () => {
        await this.runScheduledReport();
      },
      'Daily Trending Report'
    );

    this.scheduler.startAll();
  }

  /**
   * Run scheduled report for all active subscriptions
   */
  async runScheduledReport() {
    console.log('Running scheduled trending report...');

    try {
      for (const [userId, subscription] of this.subscriptions.entries()) {
        if (subscription.status === 'active') {
          const { language, since } = subscription.preferences;
          const repos = await this.scraper.getTrending(language, since);

          await this.sendNotifications(repos, subscription.channels, { language, since });
          await this.payment.logUsage(userId, 'scheduled_report');
        }
      }

      console.log('Scheduled report completed');
    } catch (error) {
      console.error('Scheduled report failed:', error);
    }
  }

  /**
   * Start the server
   */
  start() {
    this.app.listen(this.port, () => {
      console.log(`\n🚀 GitHub Trending Monitor started`);
      console.log(`📡 Server running on port ${this.port}`);
      console.log(`💰 SkillPay integration: ${this.payment.apiKey ? 'Enabled' : 'Disabled'}`);
      console.log(`📅 Scheduled tasks: ${this.scheduler.getTasks().length}`);
      console.log(`\nEndpoints:`);
      console.log(`  GET  /trending - Fetch trending repos`);
      console.log(`  POST /notify - Trigger notification`);
      console.log(`  POST /subscribe - Subscribe to daily reports`);
      console.log(`  POST /unsubscribe - Unsubscribe`);
      console.log(`  GET  /health - Health check`);
      console.log(`\n`);
    });

    // Launch Telegram bot
    if (process.env.TELEGRAM_BOT_TOKEN) {
      this.telegramNotifier.launch();
    }

    // Graceful shutdown
    process.on('SIGINT', () => {
      console.log('\nShutting down gracefully...');
      this.scheduler.stopAll();
      process.exit(0);
    });
  }
}

// Start application
if (require.main === module) {
  const monitor = new GitHubTrendingMonitor();
  monitor.start();
}

module.exports = GitHubTrendingMonitor;
