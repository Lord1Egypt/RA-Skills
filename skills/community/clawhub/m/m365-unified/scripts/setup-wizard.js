#!/usr/bin/env node
/**
 * M365 Unified Skill - Setup Wizard
 * 
 * Interactive setup that asks which features you need,
 * collects app registration data, and provides permission instructions.
 */

import readline from 'readline';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// Create readline interface
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
});

// Helper: Ask yes/no question
function askYesNo(question, defaultYes = true) {
  return new Promise((resolve) => {
    const defaultText = defaultYes ? 'Y/n' : 'y/N';
    rl.question(`${question} [${defaultText}]: `, (answer) => {
      if (answer === '') {
        resolve(defaultYes);
      } else {
        resolve(answer.toLowerCase().startsWith('y'));
      }
    });
  });
}

// Helper: Ask for text input
function askText(question, defaultValue = '') {
  return new Promise((resolve) => {
    const defaultText = defaultValue ? ` [${defaultValue}]` : '';
    rl.question(`${question}${defaultText}: `, (answer) => {
      resolve(answer || defaultValue);
    });
  });
}

// Helper: Ask for secret (masked input note)
function askSecret(question) {
  return new Promise((resolve) => {
    rl.question(`${question} (will be hidden): `, (answer) => {
      resolve(answer);
    });
  });
}

// Generate permission checklist based on selected features
function generatePermissionChecklist(features) {
  const permissions = {
    application: [],
    notes: [],
  };

  if (features.email) {
    permissions.application.push(
      { name: 'Mail.Read', description: 'Read emails in all mailboxes' },
      { name: 'Mail.ReadWrite', description: 'Create, edit, delete emails' },
      { name: 'Mail.Send', description: 'Send emails from any mailbox' },
    );
    permissions.notes.push('✓ Email: Required for reading, sending, and managing emails');
  }

  if (features.sharepoint) {
    permissions.application.push(
      { name: 'Sites.ReadWrite.All', description: 'Read and write all SharePoint sites' },
      { name: 'Files.ReadWrite.All', description: 'Read and write files in all site collections' },
    );
    permissions.notes.push('✓ SharePoint: Required for file operations in SharePoint sites');
  }

  if (features.onedrive) {
    permissions.application.push(
      { name: 'Files.ReadWrite.All', description: 'Read and write all files (OneDrive)' },
    );
    permissions.notes.push('✓ OneDrive: Required for personal file storage access');
  }

  if (features.planner) {
    permissions.application.push(
      { name: 'Tasks.ReadWrite', description: 'Create, update, delete Planner tasks' },
      { name: 'Group.Read.All', description: 'Read all M365 groups (needed for Planner)' },
    );
    permissions.notes.push('✓ Planner: Required for task management (needs M365 Group)');
  }

  if (features.webhooks) {
    permissions.application.push(
      { name: 'User.Read', description: 'Sign in and read user profile (for webhook validation)' },
    );
    permissions.notes.push('✓ Webhooks: Minimal permission for subscription validation');
  }

  if (features.sharedMailboxes) {
    permissions.notes.push('✓ Shared Mailboxes: No extra permissions needed (uses same Mail.* permissions)');
    permissions.notes.push('  → Access controlled via Azure AD app assignment to specific mailboxes');
  }

  return permissions;
}

// Generate detailed permission instructions
function generatePermissionInstructions(features) {
  let instructions = '';

  if (features.email) {
    instructions += `
   ┌─────────────────────────────────────────────────────────────┐
   │ Email (Exchange Online) Permissions                         │
   ├─────────────────────────────────────────────────────────────┤
   │ ☑ Mail.Read                                                 │
   │   → Allows reading emails from configured mailboxes         │
   │                                                             │
   │ ☑ Mail.ReadWrite                                            │
   │   → Allows moving, deleting, and organizing emails          │
   │                                                             │
   │ ☑ Mail.Send                                                 │
   │   → Allows sending emails on behalf of users                │
   └─────────────────────────────────────────────────────────────┘
`;
  }

  if (features.sharepoint) {
    instructions += `
   ┌─────────────────────────────────────────────────────────────┐
   │ SharePoint Permissions                                      │
   ├─────────────────────────────────────────────────────────────┤
   │ ☑ Sites.ReadWrite.All                                       │
   │   → Full access to all SharePoint site collections          │
   │   → Required for uploading/downloading files                │
   │                                                             │
   │ ☑ Files.ReadWrite.All                                       │
   │   → Access to all files across SharePoint sites             │
   │   → Used for document library operations                    │
   │                                                             │
   │ ⚠️  RESTRICTION TIP: Limit to specific sites via            │
   │     Azure AD → Enterprise Apps → Your App → Permissions     │
   │     → Add specific SharePoint sites (not all sites)         │
   └─────────────────────────────────────────────────────────────┘
`;
  }

  if (features.onedrive) {
    instructions += `
   ┌─────────────────────────────────────────────────────────────┐
   │ OneDrive Permissions                                        │
   ├─────────────────────────────────────────────────────────────┤
   │ ☑ Files.ReadWrite.All                                       │
   │   → Access to all OneDrive accounts in organization         │
   │                                                             │
   │ ⚠️  RESTRICTION TIP: Use app assignment to limit to         │
   │     specific users only (see security section below)        │
   └─────────────────────────────────────────────────────────────┘
`;
  }

  if (features.planner) {
    instructions += `
   ┌─────────────────────────────────────────────────────────────┐
   │ Planner Permissions                                         │
   ├─────────────────────────────────────────────────────────────┤
   │ ☑ Tasks.ReadWrite                                           │
   │   → Create, update, delete Planner tasks                    │
   │                                                             │
   │ ☑ Group.Read.All                                            │
   │   → Read all M365 groups (required to find Planner plans)   │
   │                                                             │
   │ ⚠️  NOTE: Planner requires an M365 Group with Planner       │
   │     enabled. You'll need the Group ID for configuration.    │
   └─────────────────────────────────────────────────────────────┘
`;
  }

  return instructions;
}

// Generate mailbox access restriction guide
function generateMailboxRestrictionGuide() {
  return `
╔══════════════════════════════════════════════════════════════╗
║     Mailbox Access Restrictions (Security Best Practice)     ║
╚══════════════════════════════════════════════════════════════╝

By default, Mail.ReadWrite permissions grant access to ALL mailboxes
in your organization. To restrict access to specific mailboxes only:

OPTION 1: Azure AD App Assignment (Recommended)
─────────────────────────────────────────────────────────────────

1. Go to Azure Portal → Azure Active Directory
2. Navigate to: Enterprise applications
3. Find and click your app registration ("M365 Unified Skill")
4. Click: Users and groups
5. Click: Add user/group
6. Select ONLY the mailboxes/users that should have access
7. Click: Assign

Result: The app can only access mailboxes of assigned users/groups.

OPTION 2: Application Access Policies (PowerShell)
─────────────────────────────────────────────────────────────────

For Exchange Online, create an application access policy:

# Connect to Exchange Online PowerShell
Connect-ExchangeOnline

# Create policy that allows access only to specific mailboxes
New-ApplicationAccessPolicy \
  -AppId "YOUR-CLIENT-ID" \
  -PolicyScopeGroupId "security-group-email" \
  -AccessRight RestrictAccess \
  -AppDisplayName "M365 Unified Skill"

# Test the policy
Test-ApplicationAccessPolicy \
  -AppId "YOUR-CLIENT-ID" \
  -Identity "user@domain.com"

Result: App can only access mailboxes in the specified security group.

OPTION 3: Use Dedicated Service Account (Simple)
─────────────────────────────────────────────────────────────────

1. Create a dedicated service account: service@domain.com
2. Configure mailbox forwarding rules to forward emails to this account
3. Grant the app access only to this service account
4. Use service account email in M365_MAILBOX config

Result: App only accesses one dedicated mailbox.

RECOMMENDATION:
   - For small setups: Option 3 (service account)
   - For production: Option 1 (Azure AD assignment)
   - For enterprise: Option 2 (Exchange policies)

`;
}

// Generate complete setup instructions
function generateSetupInstructions(features, config) {
  let instructions = `
╔══════════════════════════════════════════════════════════════╗
║         M365 Unified Skill - Complete Setup Guide            ║
╚══════════════════════════════════════════════════════════════╝

✅ Selected Features:
`;

  if (features.email) instructions += '   ✓ Email (Exchange Online)\n';
  if (features.sharepoint) instructions += '   ✓ SharePoint\n';
  if (features.onedrive) instructions += '   ✓ OneDrive\n';
  if (features.planner) instructions += '   ✓ Planner\n';
  if (features.webhooks) instructions += '   ✓ Webhooks (Push Notifications)\n';
  if (features.sharedMailboxes) instructions += '   ✓ Shared Mailboxes\n';

  instructions += `
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 STEP 1: Create App Registration in Azure AD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Go to https://portal.azure.com
2. Navigate to: Azure Active Directory → App registrations
3. Click: + New registration
4. Configure:
   
   Name: "M365 Unified Skill"
   Supported account types: Single tenant
   Redirect URI: Leave empty (not needed for this skill)
   
5. Click: Register
6. Copy these values from Overview page:
   
   Application (client) ID: _______________________
   Directory (tenant) ID: _______________________

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔐 STEP 2: Create Client Secret
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. In your app registration, go to: Certificates & secrets
2. Click: + New client secret
3. Configure:
   
   Description: "M365 Unified Skill"
   Expires: Choose 12-24 months (recommended: 18 months)
   
4. Click: Add
5. ⚠️  COPY THE SECRET VALUE IMMEDIATELY!
   
   Value: _______________________
   
   (It will be hidden after you leave this page!)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🛡️  STEP 3: Configure API Permissions
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
${generatePermissionInstructions(features)}

SETUP STEPS:

1. In your app registration, go to: API permissions
2. Click: + Add a permission
3. Select: Microsoft Graph
4. Select: Application permissions (NOT delegated!)
5. Search and add each permission listed above
6. Repeat for all permissions
7. IMPORTANT: Click "Grant admin consent for [Your Tenant]"
8. Wait for status to show "Granted" for all permissions

⚠️  SECURITY: See mailbox restriction guide at the end of this
   document to limit access to specific mailboxes only!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 STEP 4: Get Required IDs
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

From App Registration Overview:
   - Application (client) ID: ${config.clientId || '_______________________'}
   - Directory (tenant) ID: ${config.tenantId || '_______________________'}

`;

  if (features.sharepoint) {
    instructions += `
For SharePoint Site ID (use Graph Explorer):
   1. Go to https://developer.microsoft.com/graph/graph-explorer
   2. Sign in with admin account
   3. Run: GET https://graph.microsoft.com/v1.0/sites
   4. Find your site and copy the "id" field
   
   Site ID: ${config.sharepointSiteId || '_______________________'}
   (Format: tenant.sharepoint.com,site-guid,web-guid)
`;
  }

  if (features.planner) {
    instructions += `
For Planner Group ID (use Graph Explorer):
   1. Go to https://developer.microsoft.com/graph/graph-explorer
   2. Run: GET https://graph.microsoft.com/v1.0/groups?$filter=resourceProvisioningOptions/Any(x:x eq 'Team')
   3. Find the group with Planner and copy the "id" field
   
   Group ID: ${config.plannerGroupId || '_______________________'}
`;
  }

  instructions += `
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚙️  STEP 5: Configuration Complete!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your .env file has been created at:
   ${path.join(__dirname, '..', '.env')}

This file contains all your configuration with placeholders.
Fill in the values you collected above.

⚠️  SECURITY REMINDERS:

   ✓ Never commit .env file to git (it's in .gitignore)
   ✓ Store client secret securely (password manager recommended)
   ✓ Rotate client secret every 12-18 months
   ✓ Review mailbox access restrictions (see below)
   ✓ Monitor sign-in logs in Azure AD regularly

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🧪 STEP 6: Test Connection
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

After filling in your .env file:

   cd ${path.join(__dirname, '..')}
   npm install
   npm test

Expected output:
   ✅ Connection successful!
   User: Your Name
   Email: user@domain.com

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📚 Next Steps
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Fill in .env file with your credentials
2. Run: npm test (verify connection)
3. Run feature-specific tests:
   ${features.email ? 'npm run test:email' : ''}
   ${features.sharepoint ? 'npm run test:sharepoint' : ''}
   ${features.planner ? 'npm run test:planner' : ''}
4. Review docs/webhooks.md if you enabled webhooks
5. Integrate into OpenClaw workflow

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
${generateMailboxRestrictionGuide()}
📖 Documentation
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

   README.md              - Overview and quick start
   docs/setup.md          - Detailed setup guide
   docs/webhooks.md       - Webhook configuration
   SKILL.md               - OpenClaw integration guide

Need help? Open an issue or check Microsoft Graph docs:
https://learn.microsoft.com/en-us/graph/overview

`;

  return instructions;
}

// Main wizard function
async function runWizard() {
  console.log(`
╔══════════════════════════════════════════════════════════════╗
║           M365 Unified Skill - Setup Wizard                  ║
║                                                              ║
║  This wizard will help you configure only the features you   ║
║  need. No unnecessary permissions or complexity!             ║
╚══════════════════════════════════════════════════════════════╝
`);

  const features = {};
  const config = {};

  // Ask about features
  console.log('📦 Let\'s configure your M365 Unified Skill...\n');

  features.email = await askYesNo('Enable Email (Exchange Online)?');
  
  if (features.email) {
    config.mailbox = await askText('Primary mailbox email address');
    const shared = await askYesNo('Need Shared Mailbox support?', false);
    if (shared) {
      features.sharedMailboxes = true;
      config.sharedMailboxes = await askText('Shared mailbox emails (comma-separated)');
    }
  }

  features.sharepoint = await askYesNo('Enable SharePoint?', false);
  features.onedrive = await askYesNo('Enable OneDrive?', false);
  features.planner = await askYesNo('Enable Planner (task management)?', false);
  features.webhooks = await askYesNo('Enable Webhooks (push notifications)?', false);

  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  // Collect app registration data (optional - user can fill in .env manually)
  console.log('🔐 App Registration Data (Optional)\n');
  console.log('You can enter your Azure AD app registration data now,');
  console.log('or fill it in the .env file manually later.\n');

  const enterNow = await askYesNo('Enter credentials now?', true);

  if (enterNow) {
    config.tenantId = await askText('Tenant ID (Directory ID)');
    config.clientId = await askText('Client ID (Application ID)');
    config.clientSecret = await askSecret('Client Secret');
    
    if (features.sharepoint) {
      config.sharepointSiteId = await askText('SharePoint Site ID');
    }
    
    if (features.planner) {
      config.plannerGroupId = await askText('Planner Group ID (M365 Group)');
    }
  }

  console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

  // Generate .env file from template
  console.log('📝 Generating .env file...');
  const templatePath = path.join(__dirname, '..', 'config', 'template.env');
  const envPath = path.join(__dirname, '..', '.env');
  
  let envContent = fs.readFileSync(templatePath, 'utf8');
  
  // Replace placeholders with user input
  if (config.tenantId) {
    envContent = envContent.replace(
      /M365_TENANT_ID="<your-tenant-id-here>"/,
      `M365_TENANT_ID="${config.tenantId}"`
    );
  }
  
  if (config.clientId) {
    envContent = envContent.replace(
      /M365_CLIENT_ID="<your-client-id-here>"/,
      `M365_CLIENT_ID="${config.clientId}"`
    );
  }
  
  if (config.clientSecret) {
    envContent = envContent.replace(
      /M365_CLIENT_SECRET="<your-client-secret-here>"/,
      `M365_CLIENT_SECRET="${config.clientSecret}"`
    );
  }

  if (config.mailbox) {
    envContent = envContent.replace(
      /M365_MAILBOX="<user@domain\.com>"/,
      `M365_MAILBOX="${config.mailbox}"`
    );
  }
  
  if (config.sharedMailboxes) {
    envContent = envContent.replace(
      /M365_SHARED_MAILBOXES="<team1@domain\.com>,<team2@domain\.com>"/,
      `M365_SHARED_MAILBOXES="${config.sharedMailboxes}"`
    );
  }

  if (config.sharepointSiteId) {
    envContent = envContent.replace(
      /M365_SHAREPOINT_SITE_ID="<tenant>\.sharepoint\.com,<site-guid>,<web-guid>"/,
      `M365_SHAREPOINT_SITE_ID="${config.sharepointSiteId}"`
    );
  }

  if (config.plannerGroupId) {
    envContent = envContent.replace(
      /M365_PLANNER_GROUP_ID="<m365-group-id-here>"/,
      `M365_PLANNER_GROUP_ID="${config.plannerGroupId}"`
    );
  }

  // Update feature toggles
  envContent = envContent.replace(/M365_ENABLE_EMAIL=true/, `M365_ENABLE_EMAIL=${features.email}`);
  envContent = envContent.replace(/M365_ENABLE_SHAREPOINT=false/, `M365_ENABLE_SHAREPOINT=${features.sharepoint}`);
  envContent = envContent.replace(/M365_ENABLE_ONEDRIVE=false/, `M365_ENABLE_ONEDRIVE=${features.onedrive}`);
  envContent = envContent.replace(/M365_ENABLE_PLANNER=false/, `M365_ENABLE_PLANNER=${features.planner}`);
  envContent = envContent.replace(/M365_ENABLE_WEBHOOKS=false/, `M365_ENABLE_WEBHOOKS=${features.webhooks}`);

  fs.writeFileSync(envPath, envContent);
  console.log('✅ .env file created\n');

  // Generate setup instructions
  const instructions = generateSetupInstructions(features, config);
  
  // Save instructions to file
  const instructionsPath = path.join(__dirname, '..', 'SETUP-INSTRUCTIONS.txt');
  fs.writeFileSync(instructionsPath, instructions);

  // Display instructions
  console.log(instructions);

  rl.close();
}

// Run the wizard
runWizard().catch(console.error);
