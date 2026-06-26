// Merxex Exchange — Interactive Functionality

document.addEventListener('DOMContentLoaded', function() {

    // Smooth scroll for navigation links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                // Close mobile menu if open
                navLinks.classList.remove('open');
                menuToggle.setAttribute('aria-expanded', 'false');
            }
        });
    });

    // Mobile nav toggle
    const menuToggle = document.getElementById('navToggle');
    const navLinks = document.querySelector('.nav-links');

    if (menuToggle && navLinks) {
        menuToggle.addEventListener('click', function() {
            const isOpen = navLinks.classList.toggle('open');
            menuToggle.setAttribute('aria-expanded', String(isOpen));
        });
    }

    // Escape key closes mobile menu
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && navLinks && navLinks.classList.contains('open')) {
            navLinks.classList.remove('open');
            menuToggle.setAttribute('aria-expanded', 'false');
        }
    });

    // Navbar scroll shadow
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', function() {
        if (navbar) {
            navbar.style.boxShadow = window.pageYOffset > 60
                ? '0 2px 20px rgba(0,0,0,0.4)'
                : 'none';
        }
    }, { passive: true });

    // Contact form handler — submits to FormSubmit.co, shows loading state
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Sending...';
            // Native form submit proceeds to FormSubmit.co; no preventDefault
        });
    }

    // Show success message if redirected back after submission
    if (new URLSearchParams(window.location.search).get('contacted') === 'true') {
        const wrap = document.querySelector('.contact-form-wrap');
        if (wrap) {
            wrap.innerHTML = '<div style="padding:2rem;text-align:center;color:#a09cff;background:rgba(108,99,255,0.1);border:1px solid rgba(108,99,255,0.3);border-radius:12px"><strong>Message received.</strong><br>We\'ll respond within 24 hours.</div>';
        }
    }

    function showFormMessage(type, message) {
        let msgDiv = document.querySelector('.form-message');
        if (!msgDiv) {
            msgDiv = document.createElement('div');
            msgDiv.className = 'form-message';
            msgDiv.style.cssText = `
                padding: 1rem 1.5rem;
                border-radius: 8px;
                margin-top: 1rem;
                font-size: 0.95rem;
                text-align: center;
            `;
            contactForm.parentNode.insertBefore(msgDiv, contactForm.nextSibling);
        }

        msgDiv.textContent = message;
        msgDiv.style.background = type === 'success'
            ? 'rgba(108, 99, 255, 0.15)'
            : 'rgba(229, 62, 62, 0.15)';
        msgDiv.style.border = type === 'success'
            ? '1px solid rgba(108, 99, 255, 0.4)'
            : '1px solid rgba(229, 62, 62, 0.4)';
        msgDiv.style.color = type === 'success' ? '#a09cff' : '#fc8181';
        msgDiv.style.display = 'block';

        setTimeout(() => { msgDiv.style.display = 'none'; }, 5000);
    }

    // Fade-up animation on scroll
    const fadeObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
                fadeObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

    document.querySelectorAll('.step-card, .agent-card, .trust-item, .fee-card, .stat-item').forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(24px)';
        el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        fadeObserver.observe(el);
    });

    // Active nav link tracking
    const sections = document.querySelectorAll('section[id]');
    const navAnchors = document.querySelectorAll('.nav-links a');

    window.addEventListener('scroll', function() {
        let current = '';
        sections.forEach(section => {
            if (window.pageYOffset >= section.offsetTop - 200) {
                current = section.getAttribute('id');
            }
        });
        navAnchors.forEach(link => {
            link.classList.toggle('active', link.getAttribute('href') === `#${current}`);
        });
    }, { passive: true });

    // API code block copy-on-click
    const apiBlock = document.querySelector('.api-code');
    if (apiBlock) {
        apiBlock.style.cursor = 'pointer';
        apiBlock.title = 'Click to copy';
        apiBlock.addEventListener('click', function() {
            navigator.clipboard?.writeText(apiBlock.innerText).then(() => {
                const orig = apiBlock.style.outline;
                apiBlock.style.outline = '2px solid #6c63ff';
                setTimeout(() => { apiBlock.style.outline = orig; }, 800);
            });
        });
    }

    console.log('Merxex Exchange loaded', new Date().toISOString());
});
