/**
 * MeetingPrep — Auto-Generate Meeting Briefs
 * @author @TheShadowRose
 * @license MIT
 */

class MeetingPrep {
  constructor(options = {}) {
    this.prepLeadTime = options.prepLeadTime || 30; // minutes
  }

  generateBrief(event, context = {}) {
    const brief = {
      title: event.title || event.summary || 'Untitled Meeting',
      time: event.start || event.time,
      duration: event.duration || '30 min',
      attendees: event.attendees || [],
      location: event.location || event.link || 'TBD',
      context: [],
      agenda: [],
      prep: []
    };

    // Generate context from provided info
    if (context.previousMeeting) brief.context.push(`Last meeting: ${context.previousMeeting}`);
    if (context.relatedEmails) brief.context.push(`${context.relatedEmails.length} related emails`);
    if (context.openTasks) {
      for (const task of context.openTasks.slice(0, 5)) brief.context.push(`Open: ${task}`);
    }

    // Generate agenda from title keywords
    const title = brief.title.toLowerCase();
    if (title.includes('standup') || title.includes('sync')) {
      brief.agenda = ['Status updates', 'Blockers', 'Action items'];
    } else if (title.includes('review')) {
      brief.agenda = ['Review materials', 'Feedback', 'Next steps'];
    } else if (title.includes('planning') || title.includes('sprint')) {
      brief.agenda = ['Retrospective', 'Upcoming priorities', 'Resource allocation'];
    } else {
      brief.agenda = ['Discussion', 'Decisions needed', 'Action items'];
    }

    // Prep items
    if (context.documentsToReview) brief.prep.push('Review shared documents');
    if (brief.attendees.length > 3) brief.prep.push('Review attendee roles and recent activity');
    brief.prep.push('Check for any updates since last meeting');

    return brief;
  }

  format(brief) {
    const lines = [`📅 Meeting Brief — ${brief.title}`];
    if (brief.time) lines.push(`Time: ${brief.time}`);
    if (brief.duration) lines.push(`Duration: ${brief.duration}`);
    if (brief.attendees.length) lines.push(`Attendees: ${brief.attendees.join(', ')}`);
    if (brief.location) lines.push(`Location: ${brief.location}`);
    if (brief.context.length) { lines.push('\nCONTEXT:'); brief.context.forEach(c => lines.push(`• ${c}`)); }
    if (brief.agenda.length) { lines.push('\nAGENDA:'); brief.agenda.forEach((a, i) => lines.push(`${i+1}. ${a}`)); }
    if (brief.prep.length) { lines.push('\nPREP NEEDED:'); brief.prep.forEach(p => lines.push(`• ${p}`)); }
    return lines.join('\n');
  }
}

module.exports = { MeetingPrep };
