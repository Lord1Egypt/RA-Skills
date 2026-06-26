const fetch = (...args) => import('node-fetch').then(({ default: f }) => f(...args));

/**
 * Validate the license key against Supabase.
 * Returns { valid: boolean, message: string, trialDaysLeft?: number }
 */
async function checkLicense(licenseKey) {
  // Skip license check entirely in development mode
  if (process.env.NODE_ENV === 'development') {
    console.log('[License] Dev mode — license check skipped');
    return { valid: true, message: 'Dev mode — license check skipped' };
  }

  const supabaseUrl = process.env.SUPABASE_URL;
  const supabaseKey = process.env.SUPABASE_SERVICE_KEY || process.env.SUPABASE_ANON_KEY;

  if (!supabaseUrl || !supabaseKey) {
    console.error('Supabase config missing — skipping license check');
    return {
      valid: false,
      message: '\u26A0\uFE0F Lead Radar: License validation unavailable. Please check your configuration.',
    };
  }

  if (!licenseKey) {
    return {
      valid: false,
      message: '\u26A0\uFE0F Lead Radar: No license key configured. Get one at lead-radar.pro',
    };
  }

  try {
    const url = `${supabaseUrl}/rest/v1/licenses?key=eq.${encodeURIComponent(licenseKey)}&select=status,trial_ends_at,gemini_key`;

    const res = await fetch(url, {
      headers: {
        apikey: supabaseKey,
        Authorization: `Bearer ${supabaseKey}`,
        'Content-Type': 'application/json',
      },
    });

    if (!res.ok) {
      console.error(`License check HTTP error: ${res.status}`);
      return {
        valid: false,
        message: '\u26A0\uFE0F Lead Radar: Could not validate license. Will retry next run.',
      };
    }

    const rows = await res.json();

    if (!rows || rows.length === 0) {
      return {
        valid: false,
        message: '\u26A0\uFE0F Lead Radar: Invalid license key. Get a valid key at lead-radar.pro',
      };
    }

    const license = rows[0];

    const geminiKey = license.gemini_key || null;

    if (license.status === 'active') {
      return { valid: true, message: 'License active', geminiKey };
    }

    if (license.status === 'trial') {
      const trialEnd = new Date(license.trial_ends_at);
      const now = new Date();

      if (trialEnd > now) {
        const daysLeft = Math.ceil((trialEnd - now) / (1000 * 60 * 60 * 24));
        return {
          valid: true,
          message: `Trial: ${daysLeft} day${daysLeft === 1 ? '' : 's'} remaining`,
          trialDaysLeft: daysLeft,
          geminiKey,
        };
      }

      return {
        valid: false,
        message:
          '\u26A0\uFE0F Lead Radar: Your trial has ended. Subscribe at lead-radar.pro to continue.',
      };
    }

    if (license.status === 'cancelled') {
      return {
        valid: false,
        message:
          '\u26A0\uFE0F Lead Radar: Your subscription was cancelled. Resubscribe at lead-radar.pro',
      };
    }

    return {
      valid: false,
      message: `\u26A0\uFE0F Lead Radar: Unknown license status "${license.status}". Contact support.`,
    };
  } catch (err) {
    console.error('License check error:', err.message);
    return {
      valid: false,
      message: '\u26A0\uFE0F Lead Radar: License check failed. Will retry next run.',
    };
  }
}

module.exports = { checkLicense };
