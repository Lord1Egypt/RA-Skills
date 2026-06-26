function escapeHeader(value) {
  return String(value).replace(/[\r\n]+/g, " ").trim();
}

export function buildEmailMessage({ from, to, subject, textBody, htmlBody }) {
  if (!from || !to) {
    throw new Error("Email delivery requires both from and to addresses.");
  }

  const boundary = `mindkeeper-${Date.now()}`;
  const headers = [
    `From: ${escapeHeader(from)}`,
    `To: ${escapeHeader(to)}`,
    `Subject: ${escapeHeader(subject)}`,
    "MIME-Version: 1.0",
    `Content-Type: multipart/alternative; boundary=\"${boundary}\"`,
  ];

  return `${headers.join("\r\n")}\r\n\r\n--${boundary}\r\nContent-Type: text/plain; charset=UTF-8\r\n\r\n${textBody}\r\n\r\n--${boundary}\r\nContent-Type: text/html; charset=UTF-8\r\n\r\n${htmlBody}\r\n\r\n--${boundary}--\r\n`;
}
