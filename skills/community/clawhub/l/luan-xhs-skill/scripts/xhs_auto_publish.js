console.error('Deprecated: QR auto-publish is unreliable on current Xiaohongshu web flows.');
console.error('Use scripts/xhs_login_sms.js to establish creator-platform login, then use scripts/xhs_publish_with_saved_session.js to publish.');
process.exit(2);
