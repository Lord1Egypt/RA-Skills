// ics-generator – core logic
// ------------------------------------------------
// Exported function: run({ events, lastDate? })
// ------------------------------------------------


const crypto = require('crypto');


/**
 * Generate a fully‑qualified iCalendar (.ics) string.
 *
 * @param {Object} params
 * @param {Array}  params.events   - Array of event descriptors.
 * @param {string} [params.lastDate] - ISO‑date of the previous chunk’s final event.
 * @returns {string} The complete .ics content.
 */
export function run({ events, lastDate }) {
  // ---- Header ---------------------------------------------------------
  const header = [
    'BEGIN:VCALENDAR',
    'PRODID:-//Google Inc//Google Calendar 70.6//EN',
    'VERSION:2.0',
    'CALSCALE:GREGORIAN'
  ];


  // ---- DTSTAMP (current UTC timestamp) -------------------------------
  const dtstamp = new Date().toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';


  // ---- Helper: convert any date to YYYYMMDDTHHMMSSZ ---------------
  const formatICSDate = (dateInput) => {


// Accepts ISO string, Date object, or number (timestamp)
    const d = (dateInput instanceof Date) ? dateInput : new Date(dateInput);
    return d.toISOString().replace(/[-:]/g, '').split('.')[0] + 'Z';
  };


  // ---- Build each VEVENT block ---------------------------------------
  const vEvents = events.map(ev => {
    const uid   = `event-${crypto.randomUUID()}`;
    const start = formatICSDate(ev.start);
    const end   = formatICSDate(ev.end);


    const lines = [
      'BEGIN:VEVENT',
      `UID:${uid}`,
      `DTSTAMP:${dtstamp}`,
      `DTSTART:${start}`,
      `DTEND:${end}`,
      `SUMMARY:${ev.summary}`,
      ev.description ? `DESCRIPTION:${ev.description}` : null,
      ev.colorId ? `X-GOOGLE-CALENDAR-COLOR:${ev.colorId}` : null,
      'END:VEVENT'
    ].filter(Boolean);


    return lines.join('\n');
  });


  // ---- Footer ---------------------------------------------------------
  const trailer = ['END:VCALENDAR'];


  // Return the assembled iCalendar text
  return [...header, ...vEvents, ...trailer].join('\n');
}