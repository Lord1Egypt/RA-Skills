/**
 * Job Tracker - Google Apps Script
 * 
 * INSTALLATION:
 * 1. Open your Google Sheet
 * 2. Go to Extensions → Apps Script
 * 3. Delete any existing code in Code.gs
 * 4. Paste this entire script
 * 5. Click Save (💾 icon)
 * 6. Refresh your Google Sheet
 * 7. A new menu "🎯 Job Tracker" will appear
 * 
 * ADDING BUTTONS:
 * 1. Go to Insert → Drawing
 * 2. Create a shape/text box with button text (e.g., "➕ Add Job")
 * 3. Click Save and Close
 * 4. Click the drawing, then click the 3 dots menu → Assign script
 * 5. Enter the function name (e.g., "addJob")
 */

// ============ CONFIGURATION ============
const CONFIG = {
  JOBS_TAB: 'Jobs',
  LOGS_TAB: 'Activity Log',
  FORM_TAB: 'Add or Edit Job',
  
  // Form cell locations (Column B)
  FORM_CELLS: {
    ourJobId: 'B4',
    company: 'B5',
    role: 'B6',
    location: 'B7',
    salary: 'B8',
    source: 'B9',
    url: 'B10',
    status: 'B11',
    appliedDate: 'B12',
    contacts: 'B13',
    nextAction: 'B14',
    nextDate: 'B15'
  },
  
  // Activity Log form cells
  LOG_CELLS: {
    jobId: 'B19',
    eventType: 'B20',
    details: 'B21'
  },
  
  // Jobs tab column order (A-P)
  JOB_COLUMNS: ['ourJobId', 'employerJobId', 'company', 'role', 'location', 'salary', 
                'source', 'url', 'status', 'appliedDate', 'contacts', 'nextAction', 
                'nextDate', 'resume', 'coverLetter', 'log'],
  
  // Valid statuses
  VALID_STATUSES: ['Discovered', 'Applied', 'Screening', 'Interview', 
                   'Karat Test Scheduled', 'Offer', 'Rejected', 'Withdrawn', 
                   'Accepted', 'Closed'],
  
  // Valid event types
  VALID_EVENTS: ['discovered', 'applied', 'recruiter_contact', 'user_reply',
                 'interview_scheduled', 'interview_completed', 'test_scheduled',
                 'test_completed', 'offer_received', 'rejection', 'follow_up',
                 'status_change', 'note']
};

// ============ MENU SETUP ============
function onOpen() {
  const ui = SpreadsheetApp.getUi();
  ui.createMenu('🎯 Job Tracker')
    .addItem('➕ Add Job', 'addJob')
    .addItem('📥 Load Job to Edit', 'loadJob')
    .addItem('💾 Save Changes', 'saveJob')
    .addSeparator()
    .addItem('📝 Add Log Entry', 'addLogEntry')
    .addSeparator()
    .addItem('🧹 Clear Form', 'clearForm')
    .addItem('🔄 Refresh Next ID', 'refreshNextId')
    .addToUi();
}

// ============ UTILITY FUNCTIONS ============

/**
 * Get the form sheet
 */
function getFormSheet() {
  return SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.FORM_TAB);
}

/**
 * Get the jobs sheet
 */
function getJobsSheet() {
  return SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.JOBS_TAB);
}

/**
 * Get the logs sheet
 */
function getLogsSheet() {
  return SpreadsheetApp.getActiveSpreadsheet().getSheetByName(CONFIG.LOGS_TAB);
}

/**
 * Get form field value
 */
function getFormValue(field) {
  const sheet = getFormSheet();
  const cell = CONFIG.FORM_CELLS[field];
  if (!cell) return '';
  return sheet.getRange(cell).getValue() || '';
}

/**
 * Set form field value
 */
function setFormValue(field, value) {
  const sheet = getFormSheet();
  const cell = CONFIG.FORM_CELLS[field];
  if (cell) {
    sheet.getRange(cell).setValue(value);
  }
}

/**
 * Get log form field value
 */
function getLogFormValue(field) {
  const sheet = getFormSheet();
  const cell = CONFIG.LOG_CELLS[field];
  if (!cell) return '';
  return sheet.getRange(cell).getValue() || '';
}

/**
 * Set log form field value
 */
function setLogFormValue(field, value) {
  const sheet = getFormSheet();
  const cell = CONFIG.LOG_CELLS[field];
  if (cell) {
    sheet.getRange(cell).setValue(value);
  }
}

/**
 * Generate next job ID
 */
function getNextJobId() {
  const sheet = getJobsSheet();
  const data = sheet.getRange('A2:A1000').getValues();
  let maxNum = 0;
  
  for (const row of data) {
    const id = row[0];
    if (id && typeof id === 'string' && id.startsWith('JOB')) {
      const num = parseInt(id.replace('JOB', ''), 10);
      if (!isNaN(num) && num > maxNum) {
        maxNum = num;
      }
    }
  }
  
  return 'JOB' + String(maxNum + 1).padStart(3, '0');
}

/**
 * Find row number for a job ID
 */
function findJobRow(jobId) {
  const sheet = getJobsSheet();
  const data = sheet.getRange('A2:A1000').getValues();
  
  for (let i = 0; i < data.length; i++) {
    if (data[i][0] === jobId) {
      return i + 2; // +2 because data starts at row 2 (1-indexed)
    }
  }
  return -1;
}

/**
 * Get current timestamp
 */
function getTimestamp() {
  return Utilities.formatDate(new Date(), Session.getScriptTimeZone(), 'yyyy-MM-dd HH:mm');
}

/**
 * Validate Google Contacts links
 * Returns true if all links are valid, or shows error and returns false
 */
function validateContactLinks(contacts) {
  if (!contacts || contacts.trim() === '') return true;
  
  // Split by common delimiters (comma, semicolon, newline, space)
  const links = contacts.split(/[,;\n\s]+/).filter(l => l.trim());
  const contactsPattern = /^https:\/\/contacts\.google\.com\/person\/c[a-zA-Z0-9]+$/;
  
  const invalidLinks = [];
  for (const link of links) {
    const trimmed = link.trim();
    if (trimmed && !contactsPattern.test(trimmed)) {
      invalidLinks.push(trimmed);
    }
  }
  
  if (invalidLinks.length > 0) {
    SpreadsheetApp.getUi().alert(
      '❌ Invalid Contact Links',
      'The following are not valid Google Contacts links:\n\n' + 
      invalidLinks.join('\n') + 
      '\n\nValid format: https://contacts.google.com/person/c123456789',
      SpreadsheetApp.getUi().ButtonSet.OK
    );
    return false;
  }
  
  return true;
}

/**
 * Show toast notification
 */
function showToast(message, title) {
  SpreadsheetApp.getActiveSpreadsheet().toast(message, title || '🎯 Job Tracker', 5);
}

// ============ MAIN FUNCTIONS ============

/**
 * Add a new job from form data
 */
function addJob() {
  const company = getFormValue('company');
  const role = getFormValue('role');
  const contacts = getFormValue('contacts');
  
  // Validation
  if (!company || !role) {
    SpreadsheetApp.getUi().alert('❌ Error', 'Company and Role are required fields.', SpreadsheetApp.getUi().ButtonSet.OK);
    return;
  }
  
  // Validate contact links
  if (!validateContactLinks(contacts)) {
    return;
  }
  
  // Generate job ID
  const jobId = getNextJobId();
  
  // Get form values
  const status = getFormValue('status') || 'Discovered';
  const appliedDate = status !== 'Discovered' ? (getFormValue('appliedDate') || getTimestamp().split(' ')[0]) : '';
  
  // Build row data (columns A-O, skip P which is formula)
  const rowData = [
    jobId,                          // A: Our Job ID
    '',                             // B: Employer Job ID
    company,                        // C: Company
    role,                           // D: Role
    getFormValue('location'),       // E: Location
    getFormValue('salary'),         // F: Salary
    getFormValue('source'),         // G: Source
    getFormValue('url'),            // H: URL
    status,                         // I: Status
    appliedDate,                    // J: Applied Date
    contacts,                       // K: Contacts
    getFormValue('nextAction'),     // L: Next Action
    getFormValue('nextDate'),       // M: Next Date
    '',                             // N: Resume
    ''                              // O: Cover Letter
  ];
  
  // Append to Jobs tab
  const jobsSheet = getJobsSheet();
  const newRow = jobsSheet.getLastRow() + 1;
  jobsSheet.getRange(newRow, 1, 1, 15).setValues([rowData]);
  
  // Add formula for Log column (P)
  const logFormula = '=IFERROR(TEXTJOIN(CHAR(10),TRUE,QUERY(\'Activity Log\'!A:D,"SELECT A,C,D WHERE B=\'"&A' + newRow + '&"\' ORDER BY A DESC LIMIT 3")),"")';
  jobsSheet.getRange(newRow, 16).setFormula(logFormula);
  
  // Add initial log entry
  const logsSheet = getLogsSheet();
  logsSheet.appendRow([
    getTimestamp(),
    jobId,
    'discovered',
    'Job added: ' + role + ' at ' + company
  ]);
  
  // Clear form and show success
  clearForm();
  showToast('Created ' + jobId + ': ' + role + ' at ' + company, '✅ Job Added');
  
  // Refresh the Next ID display
  refreshNextId();
}

/**
 * Load a job into the form for editing
 */
function loadJob() {
  const jobId = getFormValue('ourJobId');
  
  if (!jobId) {
    SpreadsheetApp.getUi().alert('❌ Error', 'Enter a Job ID in the "Our Job ID" field first.', SpreadsheetApp.getUi().ButtonSet.OK);
    return;
  }
  
  const row = findJobRow(jobId);
  if (row === -1) {
    SpreadsheetApp.getUi().alert('❌ Error', 'Job not found: ' + jobId, SpreadsheetApp.getUi().ButtonSet.OK);
    return;
  }
  
  // Get job data
  const jobsSheet = getJobsSheet();
  const data = jobsSheet.getRange(row, 1, 1, 15).getValues()[0];
  
  // Populate form
  setFormValue('ourJobId', data[0]);   // A: Job ID
  // Skip B: Employer Job ID
  setFormValue('company', data[2]);     // C: Company
  setFormValue('role', data[3]);        // D: Role
  setFormValue('location', data[4]);    // E: Location
  setFormValue('salary', data[5]);      // F: Salary
  setFormValue('source', data[6]);      // G: Source
  setFormValue('url', data[7]);         // H: URL
  setFormValue('status', data[8]);      // I: Status
  setFormValue('appliedDate', data[9]); // J: Applied Date
  setFormValue('contacts', data[10]);   // K: Contacts
  setFormValue('nextAction', data[11]); // L: Next Action
  setFormValue('nextDate', data[12]);   // M: Next Date
  
  showToast('Loaded ' + jobId + ' for editing', '📥 Job Loaded');
}

/**
 * Save changes to an existing job
 */
function saveJob() {
  const jobId = getFormValue('ourJobId');
  const contacts = getFormValue('contacts');
  
  if (!jobId) {
    SpreadsheetApp.getUi().alert('❌ Error', 'No Job ID specified. Use "Load Job" first or "Add Job" for new jobs.', SpreadsheetApp.getUi().ButtonSet.OK);
    return;
  }
  
  // Validate contact links
  if (!validateContactLinks(contacts)) {
    return;
  }
  
  const row = findJobRow(jobId);
  if (row === -1) {
    // Job doesn't exist, ask to create
    const ui = SpreadsheetApp.getUi();
    const response = ui.alert(
      '🤔 Job Not Found',
      'Job ' + jobId + ' does not exist. Would you like to add it as a new job?',
      ui.ButtonSet.YES_NO
    );
    if (response === ui.Button.YES) {
      addJob();
    }
    return;
  }
  
  // Get current status to detect changes
  const jobsSheet = getJobsSheet();
  const oldStatus = jobsSheet.getRange(row, 9).getValue();
  const newStatus = getFormValue('status');
  
  // Build row data
  const rowData = [
    jobId,                          // A: Our Job ID
    '',                             // B: Employer Job ID (preserve existing)
    getFormValue('company'),        // C: Company
    getFormValue('role'),           // D: Role
    getFormValue('location'),       // E: Location
    getFormValue('salary'),         // F: Salary
    getFormValue('source'),         // G: Source
    getFormValue('url'),            // H: URL
    newStatus,                      // I: Status
    getFormValue('appliedDate'),    // J: Applied Date
    contacts,                       // K: Contacts
    getFormValue('nextAction'),     // L: Next Action
    getFormValue('nextDate'),       // M: Next Date
    '',                             // N: Resume (preserve)
    ''                              // O: Cover Letter (preserve)
  ];
  
  // Preserve employer job ID, resume, cover letter
  const existingData = jobsSheet.getRange(row, 1, 1, 15).getValues()[0];
  rowData[1] = existingData[1];  // Employer Job ID
  rowData[13] = existingData[13]; // Resume
  rowData[14] = existingData[14]; // Cover Letter
  
  // Update the row
  jobsSheet.getRange(row, 1, 1, 15).setValues([rowData]);
  
  // Log status change if status changed
  if (oldStatus !== newStatus && newStatus) {
    const logsSheet = getLogsSheet();
    logsSheet.appendRow([
      getTimestamp(),
      jobId,
      'status_change',
      'Status changed from ' + oldStatus + ' to ' + newStatus
    ]);
  }
  
  showToast('Saved changes to ' + jobId, '💾 Job Updated');
}

/**
 * Add a log entry
 */
function addLogEntry() {
  const jobId = getLogFormValue('jobId');
  const eventType = getLogFormValue('eventType');
  const details = getLogFormValue('details');
  
  // Validation
  if (!jobId) {
    SpreadsheetApp.getUi().alert('❌ Error', 'Job ID is required.', SpreadsheetApp.getUi().ButtonSet.OK);
    return;
  }
  
  if (!eventType) {
    SpreadsheetApp.getUi().alert('❌ Error', 'Event Type is required.', SpreadsheetApp.getUi().ButtonSet.OK);
    return;
  }
  
  if (!details) {
    SpreadsheetApp.getUi().alert('❌ Error', 'Details is required.', SpreadsheetApp.getUi().ButtonSet.OK);
    return;
  }
  
  // Verify job exists
  if (findJobRow(jobId) === -1) {
    SpreadsheetApp.getUi().alert('❌ Error', 'Job not found: ' + jobId, SpreadsheetApp.getUi().ButtonSet.OK);
    return;
  }
  
  // Add log entry
  const logsSheet = getLogsSheet();
  logsSheet.appendRow([
    getTimestamp(),
    jobId,
    eventType,
    details
  ]);
  
  // Clear log form fields
  setLogFormValue('jobId', '');
  setLogFormValue('eventType', '');
  setLogFormValue('details', '');
  
  showToast('Added log entry for ' + jobId, '📝 Log Added');
}

/**
 * Clear all form fields
 */
function clearForm() {
  const sheet = getFormSheet();
  
  // Clear job form fields
  for (const field in CONFIG.FORM_CELLS) {
    sheet.getRange(CONFIG.FORM_CELLS[field]).setValue('');
  }
  
  // Clear log form fields
  for (const field in CONFIG.LOG_CELLS) {
    sheet.getRange(CONFIG.LOG_CELLS[field]).setValue('');
  }
  
  // Set default status
  setFormValue('status', 'Discovered');
  
  showToast('Form cleared', '🧹 Cleared');
}

/**
 * Refresh the Next Available ID display
 */
function refreshNextId() {
  const sheet = getFormSheet();
  const nextId = getNextJobId();
  sheet.getRange('E16').setValue(nextId);
}

// ============ DATA VALIDATION SETUP ============

/**
 * Set up data validation dropdowns (run once)
 */
function setupDataValidation() {
  const sheet = getFormSheet();
  
  // Status dropdown
  const statusValidation = SpreadsheetApp.newDataValidation()
    .requireValueInList(CONFIG.VALID_STATUSES, true)
    .setAllowInvalid(false)
    .build();
  sheet.getRange(CONFIG.FORM_CELLS.status).setDataValidation(statusValidation);
  
  // Event Type dropdown
  const eventValidation = SpreadsheetApp.newDataValidation()
    .requireValueInList(CONFIG.VALID_EVENTS, true)
    .setAllowInvalid(false)
    .build();
  sheet.getRange(CONFIG.LOG_CELLS.eventType).setDataValidation(eventValidation);
  
  showToast('Data validation dropdowns added', '✅ Setup Complete');
}

// ============ OPTIONAL: KEYBOARD SHORTCUTS ============

/**
 * Handle edit events (optional - for auto-validation)
 */
function onEdit(e) {
  const sheet = e.source.getActiveSheet();
  const range = e.range;
  
  // Only process edits on the form tab
  if (sheet.getName() !== CONFIG.FORM_TAB) return;
  
  const cell = range.getA1Notation();
  
  // Auto-capitalize status
  if (cell === CONFIG.FORM_CELLS.status) {
    const value = range.getValue();
    if (value && typeof value === 'string') {
      const capitalized = value.charAt(0).toUpperCase() + value.slice(1).toLowerCase();
      if (CONFIG.VALID_STATUSES.includes(capitalized)) {
        range.setValue(capitalized);
      }
    }
  }
}
