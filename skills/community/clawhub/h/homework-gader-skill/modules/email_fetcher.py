import imaplib
import email
import os

def fetch_attachments(user, auth_code):
    mail = imaplib.IMAP4_SSL("imap.qq.com")
    mail.login(user, auth_code)
    mail.select("inbox")

    status, messages = mail.search(None, 'UNSEEN')

    file_paths = []

    for num in messages[0].split():
        typ, msg_data = mail.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])

        for part in msg.walk():
            if part.get_content_disposition() == 'attachment':
                filename = part.get_filename()

                if filename and filename.endswith(".zip"):
                    path = f"data/downloads/{filename}"

                    with open(path, 'wb') as f:
                        f.write(part.get_payload(decode=True))

                    file_paths.append(path)

    return file_paths