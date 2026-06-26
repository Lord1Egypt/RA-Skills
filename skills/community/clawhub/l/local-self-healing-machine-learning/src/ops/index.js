// Evolver Operations (local-only build).
// lifecycle.js and health_check.js removed (deployment-specific).

module.exports = {
    skillsMonitor: require('./skills_monitor'),
    cleanup: require('./cleanup'),
    trigger: require('./trigger'),
    commentary: require('./commentary'),
    selfRepair: require('./self_repair'),
};
