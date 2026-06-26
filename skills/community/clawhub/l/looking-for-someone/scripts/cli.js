#!/usr/bin/env node

/**
 * Looking for Someone - CLI Tool
 * 
 * A local missing person case management tool
 * Version: 1.0.0
 */

const fs = require('fs');
const path = require('path');
const { program } = require('commander');

// Configuration
const DATA_DIR = path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'skills-data', 'looking-for-someone');
const CASES_FILE = path.join(DATA_DIR, 'cases.json');

// Ensure data directory exists
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

// Initialize cases file if it doesn't exist
if (!fs.existsSync(CASES_FILE)) {
  fs.writeFileSync(CASES_FILE, JSON.stringify([], null, 2));
}

// Load cases
function loadCases() {
  try {
    if (!fs.existsSync(CASES_FILE)) {
      return [];
    }
    
    const data = fs.readFileSync(CASES_FILE, 'utf8');
    if (!data.trim()) {
      return [];
    }
    
    const parsed = JSON.parse(data);
    return Array.isArray(parsed) ? parsed : [];
  } catch (error) {
    console.error('Error loading cases:', error.message);
    return [];
  }
}

// Save cases
function saveCases(cases) {
  try {
    fs.writeFileSync(CASES_FILE, JSON.stringify(cases, null, 2));
    return true;
  } catch (error) {
    console.error('Error saving cases:', error.message);
    return false;
  }
}

// Generate unique ID
function generateId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

// Format date
function formatDate(dateString) {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric'
  });
}

// CLI Setup
program
  .name('looking-for-someone')
  .description('Local missing person case management tool')
  .version('1.0.0');

// Create new case
program
  .command('create')
  .description('Create a new missing person case')
  .argument('<caseData>', 'Case data as JSON string')
  .action((caseData) => {
    try {
      const caseObj = JSON.parse(caseData);
      
      // Validate required fields
      const required = ['name', 'age', 'gender', 'lastSeenDate', 'lastSeenLocation'];
      const missing = required.filter(field => !caseObj[field]);
      
      if (missing.length > 0) {
        console.error(`Missing required fields: ${missing.join(', ')}`);
        process.exit(1);
      }
      
      const cases = loadCases();
      const newCase = {
        id: generateId(),
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        status: 'active',
        clues: [],
        progress: [],
        ...caseObj
      };
      
      cases.push(newCase);
      saveCases(cases);
      
      console.log('✅ Case created successfully');
      console.log(`📋 Case ID: ${newCase.id}`);
      console.log(`👤 Name: ${newCase.name}`);
      console.log(`📅 Last seen: ${formatDate(newCase.lastSeenDate)}`);
      console.log(`📍 Location: ${newCase.lastSeenLocation}`);
      console.log('\n⚠️  Important: Contact local authorities immediately for high-risk cases.');
      
    } catch (error) {
      console.error('Error creating case:', error.message);
      process.exit(1);
    }
  });

// List all cases
program
  .command('list')
  .description('List all missing person cases')
  .action(() => {
    const cases = loadCases();
    
    if (cases.length === 0) {
      console.log('No cases found.');
      return;
    }
    
    console.log(`📊 Found ${cases.length} case(s):\n`);
    
    cases.forEach((caseItem, index) => {
      console.log(`${index + 1}. ${caseItem.name} (${caseItem.age} ${caseItem.gender})`);
      console.log(`   ID: ${caseItem.id}`);
      console.log(`   Status: ${caseItem.status}`);
      console.log(`   Last seen: ${formatDate(caseItem.lastSeenDate)} in ${caseItem.lastSeenLocation}`);
      console.log(`   Clues: ${caseItem.clues?.length || 0}`);
      console.log(`   Created: ${formatDate(caseItem.createdAt)}`);
      console.log('');
    });
  });

// View case progress
program
  .command('progress')
  .description('View progress for a specific case')
  .argument('<caseId>', 'Case ID')
  .action((caseId) => {
    const cases = loadCases();
    const caseItem = cases.find(c => c.id === caseId);
    
    if (!caseItem) {
      console.error(`Case not found with ID: ${caseId}`);
      process.exit(1);
    }
    
    console.log(`📈 Progress for: ${caseItem.name}\n`);
    console.log(`Case ID: ${caseItem.id}`);
    console.log(`Status: ${caseItem.status}`);
    console.log(`Last updated: ${formatDate(caseItem.updatedAt)}\n`);
    
    if (caseItem.progress && caseItem.progress.length > 0) {
      console.log('Progress Timeline:');
      caseItem.progress.forEach((item, index) => {
        console.log(`${index + 1}. [${formatDate(item.date)}] ${item.description}`);
      });
    } else {
      console.log('No progress entries yet.');
    }
    
    console.log('\nNext Steps:');
    console.log('1. Continue gathering information');
    console.log('2. Contact local authorities if not already done');
    console.log('3. Reach out to friends and family networks');
    console.log('4. Consider professional search assistance if needed');
  });

// Add clue to case
program
  .command('clue')
  .description('Add a clue to a case')
  .argument('<caseId>', 'Case ID')
  .argument('<clueContent>', 'Clue description')
  .action((caseId, clueContent) => {
    const cases = loadCases();
    const caseIndex = cases.findIndex(c => c.id === caseId);
    
    if (caseIndex === -1) {
      console.error(`Case not found with ID: ${caseId}`);
      process.exit(1);
    }
    
    const clue = {
      id: generateId(),
      date: new Date().toISOString(),
      content: clueContent,
      source: 'user',
      verified: false
    };
    
    if (!cases[caseIndex].clues) {
      cases[caseIndex].clues = [];
    }
    
    cases[caseIndex].clues.push(clue);
    cases[caseIndex].updatedAt = new Date().toISOString();
    
    // Add progress entry
    if (!cases[caseIndex].progress) {
      cases[caseIndex].progress = [];
    }
    
    cases[caseIndex].progress.push({
      date: new Date().toISOString(),
      description: `Clue added: ${clueContent.substring(0, 50)}...`
    });
    
    saveCases(cases);
    
    console.log('✅ Clue added successfully');
    console.log(`📝 Case: ${cases[caseIndex].name}`);
    console.log(`🔍 Clue: ${clueContent}`);
    console.log(`📅 Added: ${formatDate(clue.date)}`);
    console.log('\n💡 Tip: Verify clues with multiple sources when possible.');
  });

// Generate notice
program
  .command('notice')
  .description('Generate missing person notice')
  .argument('<caseId>', 'Case ID')
  .argument('[format]', 'Notice format', 'general')
  .action((caseId, format) => {
    const cases = loadCases();
    const caseItem = cases.find(c => c.id === caseId);
    
    if (!caseItem) {
      console.error(`Case not found with ID: ${caseId}`);
      process.exit(1);
    }
    
    const formats = ['general', 'wechat', 'weibo', 'douyin', 'official'];
    if (!formats.includes(format)) {
      console.error(`Invalid format. Choose from: ${formats.join(', ')}`);
      process.exit(1);
    }
    
    console.log(`📢 Missing Person Notice (${format} format)\n`);
    console.log('=' .repeat(50));
    
    switch (format) {
      case 'general':
        generateGeneralNotice(caseItem);
        break;
      case 'wechat':
        generateWeChatNotice(caseItem);
        break;
      case 'weibo':
        generateWeiboNotice(caseItem);
        break;
      case 'douyin':
        generateDouyinNotice(caseItem);
        break;
      case 'official':
        generateOfficialNotice(caseItem);
        break;
    }
    
    console.log('=' .repeat(50));
    console.log('\n⚠️  Safety Reminders:');
    console.log('- Share responsibly');
    console.log('- Respect privacy');
    console.log('- Contact authorities with credible information');
    console.log('- Be cautious of scams');
  });

// Get search guidance
program
  .command('guide')
  .description('Get search guidance and recommendations')
  .action(() => {
    console.log('🔍 Missing Person Search Guidance\n');
    console.log('Immediate Actions:');
    console.log('1. ✅ Contact local police (dial 110 in China)');
    console.log('2. ✅ Provide all available information');
    console.log('3. ✅ Designate a family spokesperson');
    console.log('4. ✅ Secure personal belongings for evidence');
    console.log('5. ✅ Document all communications\n');
    
    console.log('Search Strategies:');
    console.log('• Check hospitals and clinics');
    console.log('• Contact friends and acquaintances');
    console.log('• Review recent communications');
    console.log('• Check transportation records');
    console.log('• Search regular locations\n');
    
    console.log('Online Resources:');
    console.log('• Local police websites');
    console.log('• Community social media groups');
    console.log('• Missing person registries');
    console.log('• Volunteer search organizations\n');
    
    console.log('⚠️  High-Risk Indicators (Require Immediate Action):');
    console.log('- Minors under 14 years old');
    console.log('- Elderly with dementia or health issues');
    console.log('- Mental health crisis situations');
    console.log('- Self-harm threats or attempts');
    console.log('- Missing for more than 48 hours');
  });

// Show safety reminders
program
  .command('reminders')
  .description('Show safety and fraud prevention reminders')
  .action(() => {
    console.log('🛡️  Safety and Fraud Prevention Reminders\n');
    
    console.log('🚨 Red Flags (Report Immediately):');
    console.log('1. Requests for payment in exchange for information');
    console.log('2. Demands for upfront transfers, deposits, or donations');
    console.log('3. Requests for ID cards, bank cards, or verification codes');
    console.log('4. Claims of being police without verifiable identification');
    console.log('5. Requests to download unknown apps or enable screen sharing');
    console.log('6. Pressure to act quickly without verification\n');
    
    console.log('✅ Safe Practices:');
    console.log('• Verify all information through official channels');
    console.log('• Use dedicated contact methods for the search');
    console.log('• Document all communications');
    console.log('• Consult with authorities on significant leads');
    console.log('• Protect personal and financial information\n');
    
    console.log('📞 Emergency Contacts:');
    console.log('• Police: 110 (China)');
    console.log('• Medical Emergency: 120 (China)');
    console.log('• Fire Department: 119 (China)');
    console.log('• Local missing person organizations');
  });

// Notice generation functions
function generateGeneralNotice(caseItem) {
  console.log(`MISSING: ${caseItem.name}`);
  console.log(`Age: ${caseItem.age} | Gender: ${caseItem.gender}`);
  console.log(`Last Seen: ${formatDate(caseItem.lastSeenDate)}`);
  console.log(`Location: ${caseItem.lastSeenLocation}`);
  
  if (caseItem.clothing) {
    console.log(`Clothing: ${caseItem.clothing}`);
  }
  
  if (caseItem.distinguishingFeatures) {
    console.log(`Distinguishing Features: ${caseItem.distinguishingFeatures}`);
  }
  
  console.log('\nIf you have any information, please contact local authorities.');
  console.log('Do not approach directly if you feel unsafe.');
}

function generateWeChatNotice(caseItem) {
  console.log(`【寻人启事】${caseItem.name}`);
  console.log(`年龄：${caseItem.age}岁 | 性别：${caseItem.gender}`);
  console.log(`失踪时间：${formatDate(caseItem.lastSeenDate)}`);
  console.log(`失踪地点：${caseItem.lastSeenLocation}`);
  
  if (caseItem.clothing) {
    console.log(`衣着特征：${caseItem.clothing}`);
  }
  
  console.log('\n如有线索，请立即联系当地警方。');
  console.log('请帮忙转发，谢谢！');
  console.log('#寻人 #missingperson');
}

function generateWeiboNotice(caseItem) {
  console.log(`#寻人启事# ${caseItem.name}`);
  console.log(`年龄：${caseItem.age}岁`);
  console.log(`失踪时间：${formatDate(caseItem.lastSeenDate)}`);
  console.log(`失踪地点：${caseItem.lastSeenLocation}`);
  
  if (caseItem.distinguishingFeatures) {
    console.log(`特征：${caseItem.distinguishingFeatures}`);
  }
  
  console.log('\n如有任何信息，请私信或联系警方。');
  console.log('请帮忙扩散，感谢！');
  console.log('@当地警方 @寻人志愿者');
}

function generateDouyinNotice(caseItem) {
  console.log(`寻人：${caseItem.name}`);
  console.log(`${caseItem.age}岁，${formatDate(caseItem.lastSeenDate)}失踪`);
  console.log(`地点：${caseItem.lastSeenLocation}`);
  
  if (caseItem.clothing) {
    console.log(`穿着：${caseItem.clothing}`);
  }
  
  console.log('\n请帮忙寻找，有线索请联系！');
  console.log('#寻人 #帮助 #正能量');
}

function generateOfficialNotice(caseItem) {
  console.log('OFFICIAL MISSING PERSON NOTICE');
  console.log('=' .repeat(40));
  console.log(`NAME: ${caseItem.name.toUpperCase()}`);
  console.log(`DATE OF BIRTH: ${caseItem.birthDate || 'Not provided'}`);
  console.log(`AGE: ${caseItem.age}`);
  console.log(`GENDER: ${caseItem.gender}`);
  console.log(`HEIGHT: ${caseItem.height || 'Not provided'} cm`);
  console.log(`LAST SEEN: ${formatDate(caseItem.lastSeenDate)}`);
  console.log(`LOCATION: ${caseItem.lastSeenLocation}`);
  console.log(`CIRCUMSTANCES: ${caseItem.circumstances || 'Under investigation'}`);
  console.log('=' .repeat(40));
  console.log('\nCONTACT LOCAL POLICE WITH ANY INFORMATION');
  console.log('CASE REFERENCE: MP-' + caseItem.id.substring(0, 8).toUpperCase());
}

// Parse command line arguments
program.parse();

// Show help if no arguments
if (process.argv.length <= 2) {
  program.help();
}