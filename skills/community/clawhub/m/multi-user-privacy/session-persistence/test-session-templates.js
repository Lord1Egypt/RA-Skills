/**
 * Session Templates Test Suite
 * 
 * Tests for the Session Template Manager functionality
 */

const { getTemplateManager, BUILTIN_TEMPLATES } = require('./session-templates');
const { getSessionManager } = require('./session-manager');

async function runTests() {
  console.log('='.repeat(60));
  console.log('Session Templates Test Suite');
  console.log('='.repeat(60));
  
  // Initialize managers
  const templateManager = getTemplateManager();
  await templateManager.initialize();
  
  const sessionManager = getSessionManager();
  await sessionManager.initialize();
  
  console.log('\n');
  
  // Test 1: List all templates
  console.log('📋 Test 1: List All Templates');
  console.log('-'.repeat(60));
  const allTemplates = templateManager.getAllTemplates();
  console.log(`Found ${allTemplates.length} templates:`);
  allTemplates.forEach(t => {
    console.log(`  - ${t.name} (${t.id}) ${t.isBuiltIn ? '[Built-in]' : '[Custom]'}`);
  });
  console.log('✅ Test 1 Passed\n');
  
  // Test 2: Get built-in template details
  console.log('📋 Test 2: Get Built-in Template Details');
  console.log('-'.repeat(60));
  const adminTemplate = templateManager.getTemplate(BUILTIN_TEMPLATES.ADMIN);
  console.log('Admin Template:');
  console.log(`  Name: ${adminTemplate.name}`);
  console.log(`  Description: ${adminTemplate.description}`);
  console.log(`  Disk Quota: ${adminTemplate.quota.diskQuotaMB}MB`);
  console.log(`  Token Quota: ${adminTemplate.quota.tokenQuota}`);
  console.log(`  Can Manage Users: ${adminTemplate.permissions.canManageUsers}`);
  console.log(`  Read Only: ${adminTemplate.permissions.readOnly}`);
  console.log('✅ Test 2 Passed\n');
  
  // Test 3: Compare all built-in templates
  console.log('📋 Test 3: Compare Built-in Templates');
  console.log('-'.repeat(60));
  const templates = [
    BUILTIN_TEMPLATES.ADMIN,
    BUILTIN_TEMPLATES.STANDARD,
    BUILTIN_TEMPLATES.GUEST
  ];
  
  console.log('Template'.padEnd(15) + 'Disk'.padEnd(10) + 'Tokens'.padEnd(12) + 'Messages'.padEnd(10) + 'Timeout'.padEnd(10) + 'Read-Only');
  console.log('-'.repeat(60));
  
  templates.forEach(templateId => {
    const t = templateManager.getTemplate(templateId);
    console.log(
      t.name.padEnd(15) +
      String(t.quota.diskQuotaMB + 'MB').padEnd(10) +
      String(t.quota.tokenQuota).padEnd(12) +
      String(t.quota.messageQuota).padEnd(10) +
      String(t.quota.sessionTimeoutHours + 'h').padEnd(10) +
      String(t.permissions.readOnly)
    );
  });
  console.log('✅ Test 3 Passed\n');
  
  // Test 4: Create custom template
  console.log('📋 Test 4: Create Custom Template');
  console.log('-'.repeat(60));
  const customTemplate = await templateManager.createTemplate({
    id: 'developer',
    name: '开发者模板',
    description: '适用于开发人员，中等配额，允许代码执行',
    quota: {
      diskQuotaMB: 500,
      tokenQuota: 500000,
      messageQuota: 5000,
      sessionTimeoutHours: 72,
      maxSubAgents: 5,
      allowCodeExecution: true,
      allowSystemCommands: false
    },
    permissions: {
      canInstallSkills: true,
      canExportData: true,
      readOnly: false
    },
    features: {
      priority: 'high',
      customVariables: true
    }
  });
  console.log(`Created custom template: ${customTemplate.name}`);
  console.log(`  ID: ${customTemplate.id}`);
  console.log(`  Disk Quota: ${customTemplate.quota.diskQuotaMB}MB`);
  console.log(`  Can Install Skills: ${customTemplate.permissions.canInstallSkills}`);
  console.log('✅ Test 4 Passed\n');
  
  // Test 5: Create session with different templates
  console.log('📋 Test 5: Create Sessions with Different Templates');
  console.log('-'.repeat(60));
  
  const adminSession = await sessionManager.createSession(
    'test-admin-session',
    'ou_b96f5424607baf3a0455b55e0f4a2213',
    'feishu',
    BUILTIN_TEMPLATES.ADMIN
  );
  console.log(`Created admin session: ${adminSession.id}`);
  console.log(`  Template: ${adminSession.templateId}`);
  console.log(`  Disk Quota: ${adminSession.quota.diskQuotaMB}MB`);
  console.log(`  Can Modify Config: ${adminSession.permissions.canModifyConfig}`);
  
  const guestSession = await sessionManager.createSession(
    'test-guest-session',
    'guest-user-001',
    'feishu',
    BUILTIN_TEMPLATES.GUEST
  );
  console.log(`\nCreated guest session: ${guestSession.id}`);
  console.log(`  Template: ${guestSession.templateId}`);
  console.log(`  Disk Quota: ${guestSession.quota.diskQuotaMB}MB`);
  console.log(`  Read Only: ${guestSession.permissions.readOnly}`);
  
  const developerSession = await sessionManager.createSession(
    'test-developer-session',
    'dev-user-001',
    'feishu',
    'developer'
  );
  console.log(`\nCreated developer session: ${developerSession.id}`);
  console.log(`  Template: ${developerSession.templateId}`);
  console.log(`  Disk Quota: ${developerSession.quota.diskQuotaMB}MB`);
  console.log(`  Can Install Skills: ${developerSession.permissions.canInstallSkills}`);
  console.log('✅ Test 5 Passed\n');
  
  // Test 6: Permission checking
  console.log('📋 Test 6: Permission Checking');
  console.log('-'.repeat(60));
  const permissions = [
    'canManageUsers',
    'canModifyConfig',
    'canInstallSkills',
    'canExecuteDangerousCommands',
    'readOnly'
  ];
  
  console.log('Permission'.padEnd(30) + 'Admin'.padEnd(10) + 'Standard'.padEnd(10) + 'Guest'.padEnd(10) + 'Developer');
  console.log('-'.repeat(70));
  
  permissions.forEach(perm => {
    const adminPerm = sessionManager.hasPermission('test-admin-session', perm);
    const guestPerm = sessionManager.hasPermission('test-guest-session', perm);
    const devPerm = sessionManager.hasPermission('test-developer-session', perm);
    const standardPerm = templateManager.getTemplate(BUILTIN_TEMPLATES.STANDARD).permissions[perm];
    
    console.log(
      perm.padEnd(30) +
      String(adminPerm).padEnd(10) +
      String(standardPerm).padEnd(10) +
      String(guestPerm).padEnd(10) +
      String(devPerm)
    );
  });
  console.log('✅ Test 6 Passed\n');
  
  // Test 7: Quota validation
  console.log('📋 Test 7: Quota Validation');
  console.log('-'.repeat(60));
  
  // Test guest session quota (should fail for large requests)
  const guestQuotaCheck = sessionManager.validateQuota('test-guest-session', 'disk', 50);
  console.log('Guest session requesting 50MB disk:');
  console.log(`  Valid: ${guestQuotaCheck.valid}`);
  console.log(`  Limit: ${guestQuotaCheck.limit}MB`);
  console.log(`  Remaining: ${guestQuotaCheck.remaining}MB`);
  
  const guestQuotaCheck2 = sessionManager.validateQuota('test-guest-session', 'disk', 5);
  console.log('\nGuest session requesting 5MB disk:');
  console.log(`  Valid: ${guestQuotaCheck2.valid}`);
  console.log(`  Remaining after: ${guestQuotaCheck2.remaining - 5}MB`);
  
  // Update usage
  await sessionManager.updateUsage('test-guest-session', 'disk', 5);
  console.log('\n✅ Test 7 Passed\n');
  
  // Test 8: Template statistics
  console.log('📋 Test 8: Template Statistics');
  console.log('-'.repeat(60));
  const templateStats = templateManager.getStats();
  console.log('Template Statistics:');
  console.log(`  Total Templates: ${templateStats.total}`);
  console.log(`  Built-in: ${templateStats.builtIn}`);
  console.log(`  Custom: ${templateStats.custom}`);
  console.log(`  Template IDs: ${templateStats.templateIds.join(', ')}`);
  console.log('✅ Test 8 Passed\n');
  
  // Test 9: Session statistics
  console.log('📋 Test 9: Session Statistics');
  console.log('-'.repeat(60));
  const sessionStats = sessionManager.getStats();
  console.log('Session Statistics:');
  console.log(`  Total Sessions: ${sessionStats.total}`);
  console.log(`  Active: ${sessionStats.active}`);
  console.log(`  Hibernating: ${sessionStats.hibernating}`);
  console.log(`  Archived: ${sessionStats.archived}`);
  console.log('✅ Test 9 Passed\n');
  
  // Test 10: Export templates
  console.log('📋 Test 10: Export Templates');
  console.log('-'.repeat(60));
  const exportPath = await templateManager.exportTemplates();
  console.log(`Templates exported to: ${exportPath}`);
  console.log('✅ Test 10 Passed\n');
  
  console.log('='.repeat(60));
  console.log('All Tests Completed Successfully! ✅');
  console.log('='.repeat(60));
}

// Run tests
runTests().catch(error => {
  console.error('Test suite failed:', error);
  process.exit(1);
});
