/**
 * PRASÓWKA 2025/2026 — ULTRANOWOCZESNY UI
 * Vanilla JS — no frameworks needed
 */

(function() {
  'use strict';

  // === STATE ===
  const state = {
    theme: localStorage.getItem('prasowka-theme') || 'auto',
    scrollProgress: 0,
    isRefreshing: false,
    readArticles: JSON.parse(localStorage.getItem('prasowka-read') || '[]'),
    bookmarks: JSON.parse(localStorage.getItem('prasowka-bookmarks') || '[]')
  };

  // === DOM CACHE ===
  const $ = (selector, context = document) => context.querySelector(selector);
  const $$ = (selector, context = document) => Array.from(context.querySelectorAll(selector));

  // === THEME MANAGER ===
  const ThemeManager = {
    init() {
      this.applyTheme(state.theme);
      this.bindEvents();
      this.setupSystemListener();
    },

    applyTheme(theme) {
      const root = document.documentElement;
      
      if (theme === 'auto') {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        root.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
      } else {
        root.setAttribute('data-theme', theme);
      }
      
      // Update toggle state
      const toggle = $('.theme-toggle');
      if (toggle) {
        toggle.setAttribute('data-active', theme === 'dark' || 
          (theme === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches));
      }
    },

    toggle() {
      const current = document.documentElement.getAttribute('data-theme');
      const newTheme = current === 'dark' ? 'light' : 'dark';
      state.theme = newTheme;
      localStorage.setItem('prasowka-theme', newTheme);
      this.applyTheme(newTheme);
      
      // Trigger toast
      Toast.show(`Switched to ${newTheme === 'dark' ? '🌙 Dark' : '☀️ Light'} mode`, 'success');
    },

    bindEvents() {
      const toggle = $('.theme-toggle');
      if (toggle) {
        toggle.addEventListener('click', () => this.toggle());
      }
    },

    setupSystemListener() {
      if (state.theme === 'auto') {
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
          document.documentElement.setAttribute('data-theme', e.matches ? 'dark' : 'light');
        });
      }
    }
  };

  // === SCROLL MANAGER ===
  const ScrollManager = {
    init() {
      this.bindEvents();
      this.createProgressBar();
      this.createBackToTop();
    },

    bindEvents() {
      let ticking = false;
      
      window.addEventListener('scroll', () => {
        if (!ticking) {
          requestAnimationFrame(() => {
            this.updateProgress();
            this.toggleBackToTop();
            ticking = false;
          });
          ticking = true;
        }
      }, { passive: true });

      // Smooth scroll for nav links
      $$('.nav-item[href^="#"]').forEach(link => {
        link.addEventListener('click', (e) => {
          e.preventDefault();
          const target = $(link.getAttribute('href'));
          if (target) {
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
          }
        });
      });
    },

    createProgressBar() {
      const bar = document.createElement('div');
      bar.className = 'scroll-progress';
      document.body.appendChild(bar);
    },

    updateProgress() {
      const bar = $('.scroll-progress');
      if (!bar) return;
      
      const scrollTop = window.scrollY;
      const docHeight = document.documentElement.scrollHeight - window.innerHeight;
      const progress = (scrollTop / docHeight) * 100;
      
      bar.style.width = `${progress}%`;
      state.scrollProgress = progress;
    },

    createBackToTop() {
      const btn = document.createElement('button');
      btn.className = 'back-to-top';
      btn.innerHTML = '↑';
      btn.setAttribute('aria-label', 'Back to top');
      btn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
      });
      document.body.appendChild(btn);
    },

    toggleBackToTop() {
      const btn = $('.back-to-top');
      if (!btn) return;
      
      if (window.scrollY > 500) {
        btn.classList.add('visible');
      } else {
        btn.classList.remove('visible');
      }
    }
  };

  // === LAZY LOADING ===
  const LazyLoader = {
    init() {
      if ('IntersectionObserver' in window) {
        this.setupObserver();
      } else {
        this.loadAllImages();
      }
    },

    setupObserver() {
      const options = {
        root: null,
        rootMargin: '50px',
        threshold: 0.01
      };

      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            this.loadImage(entry.target);
            observer.unobserve(entry.target);
          }
        });
      }, options);

      $$('.lazy-image').forEach(img => observer.observe(img));
    },

    loadImage(img) {
      const src = img.dataset.src;
      if (!src) return;
      
      // Create a new image to preload
      const preload = new Image();
      preload.onload = () => {
        img.src = src;
        img.classList.add('loaded');
      };
      preload.onerror = () => {
        img.classList.add('error');
        img.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1 1"></svg>';
      };
      preload.src = src;
    },

    loadAllImages() {
      $$('.lazy-image').forEach(img => this.loadImage(img));
    }
  };

  // === REFRESH MANAGER ===
  const RefreshManager = {
    init() {
      this.bindEvents();
    },

    bindEvents() {
      const btn = $('.refresh-btn');
      if (btn) {
        btn.addEventListener('click', () => this.refresh());
      }
    },

    async refresh() {
      if (state.isRefreshing) return;
      
      state.isRefreshing = true;
      const btn = $('.refresh-btn');
      btn.classList.add('spinning');
      
      Toast.show('🔄 Refreshing news...', 'info');
      
      try {
        // Simulate refresh - in production, this would fetch new data
        await this.simulateNetworkRequest(1500);
        
        // Reload page
        window.location.reload();
      } catch (error) {
        Toast.show('❌ Refresh failed', 'error');
        state.isRefreshing = false;
        btn.classList.remove('spinning');
      }
    },

    simulateNetworkRequest(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
    }
  };

  // === BOOKMARK MANAGER ===
  const BookmarkManager = {
    init() {
      this.bindEvents();
      this.updateUI();
    },

    bindEvents() {
      $$('.action-btn[data-action="bookmark"]').forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.stopPropagation();
          const url = btn.closest('.article-card').dataset.url;
          this.toggle(url);
        });
      });
    },

    toggle(url) {
      const index = state.bookmarks.indexOf(url);
      
      if (index === -1) {
        state.bookmarks.push(url);
        Toast.show('🔖 Bookmarked!', 'success');
      } else {
        state.bookmarks.splice(index, 1);
        Toast.show('🗑️ Removed from bookmarks', 'info');
      }
      
      localStorage.setItem('prasowka-bookmarks', JSON.stringify(state.bookmarks));
      this.updateUI();
    },

    updateUI() {
      $$('.article-card').forEach(card => {
        const url = card.dataset.url;
        const btn = card.querySelector('[data-action="bookmark"]');
        if (btn) {
          const isBookmarked = state.bookmarks.includes(url);
          btn.style.color = isBookmarked ? 'var(--accent-primary)' : '';
          btn.innerHTML = isBookmarked ? '★' : '☆';
        }
      });
    }
  };

  // === SHARE MANAGER ===
  const ShareManager = {
    init() {
      this.bindEvents();
    },

    bindEvents() {
      $$('.action-btn[data-action="share"]').forEach(btn => {
        btn.addEventListener('click', async (e) => {
          e.stopPropagation();
          const card = btn.closest('.article-card');
          const url = card.dataset.url;
          const title = card.querySelector('.article-title').textContent;
          
          await this.share({ url, title });
        });
      });
    },

    async share({ url, title }) {
      if (navigator.share) {
        try {
          await navigator.share({
            title: title || 'Prasówka News',
            text: 'Check out this article from Prasówka',
            url: url
          });
          Toast.show('✅ Shared!', 'success');
        } catch (err) {
          if (err.name !== 'AbortError') {
            this.fallbackShare(url);
          }
        }
      } else {
        this.fallbackShare(url);
      }
    },

    fallbackShare(url) {
      navigator.clipboard.writeText(url).then(() => {
        Toast.show('📋 Link copied to clipboard!', 'success');
      }).catch(() => {
        Toast.show('❌ Failed to copy link', 'error');
      });
    }
  };

  // === READING TIME ESTIMATOR ===
  const ReadingTime = {
    init() {
      $$('.article-card').forEach(card => {
        const summary = card.querySelector('.article-summary');
        if (summary) {
          const words = summary.textContent.split(/\s+/).length;
          const minutes = Math.ceil(words / 200);
          
          const meta = card.querySelector('.article-meta');
          if (meta) {
            const timeBadge = document.createElement('span');
            timeBadge.className = 'reading-time';
            timeBadge.textContent = `⏱️ ${minutes} min`;
            timeBadge.style.cssText = 'margin-left: auto; font-size: 0.75rem; color: var(--text-tertiary);';
            meta.appendChild(timeBadge);
          }
        }
      });
    }
  };

  // === ANIMATION OBSERVER ===
  const AnimationObserver = {
    init() {
      if (!('IntersectionObserver' in window)) {
        $$('.article-card').forEach(el => el.classList.add('loaded'));
        return;
      }

      const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
          if (entry.isIntersecting) {
            setTimeout(() => {
              entry.target.classList.add('loaded');
            }, index * 50);
            observer.unobserve(entry.target);
          }
        });
      }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
      });

      $$('.article-card').forEach(card => {
        card.classList.add('loading');
        observer.observe(card);
      });
    }
  };

  // === TOAST NOTIFICATIONS ===
  const Toast = {
    container: null,

    init() {
      this.container = document.createElement('div');
      this.container.className = 'toast-container';
      document.body.appendChild(this.container);
    },

    show(message, type = 'info') {
      if (!this.container) this.init();

      const toast = document.createElement('div');
      toast.className = `toast ${type}`;
      toast.textContent = message;
      
      this.container.appendChild(toast);

      // Remove after animation
      setTimeout(() => {
        toast.remove();
      }, 4000);
    }
  };

  // === PWA MANAGER ===
  const PWAManager = {
    deferredPrompt: null,

    init() {
      this.bindEvents();
      this.registerServiceWorker();
    },

    bindEvents() {
      window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        this.deferredPrompt = e;
        this.showInstallPrompt();
      });

      window.addEventListener('appinstalled', () => {
        Toast.show('🎉 Prasówka installed!', 'success');
        this.deferredPrompt = null;
      });
    },

    registerServiceWorker() {
      if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('./sw.js').catch(() => {
          // Silent fail for now
        });
      }
    },

    showInstallPrompt() {
      // Only show if not already installed and prompt not dismissed recently
      const lastDismissed = localStorage.getItem('pwa-prompt-dismissed');
      if (lastDismissed && Date.now() - parseInt(lastDismissed) < 7 * 24 * 60 * 60 * 1000) {
        return;
      }

      const prompt = document.createElement('div');
      prompt.className = 'pwa-prompt';
      prompt.innerHTML = `
        <span class="pwa-prompt-icon">📱</span>
        <div class="pwa-prompt-text">
          <div class="pwa-prompt-title">Install Prasówka</div>
          <div class="pwa-prompt-subtitle">Add to home screen for quick access</div>
        </div>
        <button class="pwa-prompt-btn">Install</button>
        <button class="pwa-prompt-close">✕</button>
      `;

      document.body.appendChild(prompt);

      setTimeout(() => prompt.classList.add('visible'), 1000);

      prompt.querySelector('.pwa-prompt-btn').addEventListener('click', async () => {
        if (this.deferredPrompt) {
          this.deferredPrompt.prompt();
          const { outcome } = await this.deferredPrompt.userChoice;
          if (outcome === 'accepted') {
            Toast.show('Installing...', 'info');
          }
          this.deferredPrompt = null;
        }
        prompt.remove();
      });

      prompt.querySelector('.pwa-prompt-close').addEventListener('click', () => {
        localStorage.setItem('pwa-prompt-dismissed', Date.now().toString());
        prompt.classList.remove('visible');
        setTimeout(() => prompt.remove(), 300);
      });
    }
  };

  // === KEYBOARD NAVIGATION ===
  const KeyboardNav = {
    init() {
      document.addEventListener('keydown', (e) => {
        // '/' to search/focus
        if (e.key === '/' && !e.target.matches('input, textarea')) {
          e.preventDefault();
          this.focusSearch();
        }

        // 'r' to refresh
        if (e.key === 'r' && !e.target.matches('input, textarea')) {
          e.preventDefault();
          RefreshManager.refresh();
        }

        // 't' to toggle theme
        if (e.key === 't' && !e.target.matches('input, textarea')) {
          e.preventDefault();
          ThemeManager.toggle();
        }

        // 'Escape' to close modals/toasts
        if (e.key === 'Escape') {
          this.closeOverlays();
        }
      });
    },

    focusSearch() {
      const searchInput = $('#search-input');
      if (searchInput) {
        searchInput.focus();
      }
    },

    closeOverlays() {
      $$('.pwa-prompt').forEach(el => el.remove());
    }
  };

  // === VISIBILITY API ===
  const VisibilityManager = {
    init() {
      document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
          // Page hidden - pause any animations if needed
        } else {
          // Page visible - could refresh data if stale
          const lastUpdate = localStorage.getItem('prasowka-last-update');
          if (lastUpdate && Date.now() - parseInt(lastUpdate) > 5 * 60 * 1000) {
            // Data is older than 5 minutes, could auto-refresh
          }
        }
      });
    }
  };

  // === INITIALIZATION ===
  function init() {
    // Check for reduced motion preference
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReducedMotion) {
      document.documentElement.classList.add('reduced-motion');
    }

    // Initialize all modules
    ThemeManager.init();
    ScrollManager.init();
    LazyLoader.init();
    RefreshManager.init();
    BookmarkManager.init();
    ShareManager.init();
    ReadingTime.init();
    AnimationObserver.init();
    Toast.init();
    PWAManager.init();
    KeyboardNav.init();
    VisibilityManager.init();

    // Save timestamp
    localStorage.setItem('prasowka-last-update', Date.now().toString());

    console.log('🗞️ Prasówka 2025 loaded successfully!');
    console.log('Keyboard shortcuts: / = search, r = refresh, t = theme, esc = close');
  }

  // Run when DOM is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }

})();
