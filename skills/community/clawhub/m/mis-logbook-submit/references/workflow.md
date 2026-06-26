# Daily MIS logbook workflow

## Inputs

- Current date in `Asia/Jakarta` / WIB.
- Activity source from the same day's GitHub and GitLab commits.
- Local MIS credentials file. By default the submitter reads `~/.openclaw/secrets/mis.env`, or `MIS_ENV_FILE` if set.
- Destination page: `Akademik -> Entry Logbook KP` on `online.mis.pens.ac.id`.

## Approval-first flow

1. Generate and synthesize the day's activity text.
2. Send the draft to the user first.
3. Wait for explicit confirmation.
4. Only then submit the saved draft to MIS.
5. If there is no confirmation yet, do not submit.

## Proven navigation path

1. Open `https://online.mis.pens.ac.id`.
2. Choose `Login -> Mahasiswa/Dosen/Staff`.
3. Expect redirect to CAS at `https://login.pens.ac.id/cas/login?...`.
4. Log in with local secrets.
5. After login, open `Akademik -> Entry Logbook KP`.
6. Expected entry page URL shape:
   - `https://online.mis.pens.ac.id/entry_logbook_kp1.php?...`
7. The page is `MONITORING HARIAN KERJA PRAKTEK`.

## Proven form behavior

Visible fields/controls on the entry page include:

- `Tanggal`
- `Jam Mulai`
- `Jam Selesai`
- `Kegiatan/Materi`
- `Apakah kegiatan ... sesuai dengan mata kuliah ...?` with `Ya` / `Tidak`
- `Pilih Matakuliah` when `Ya`
- declaration checkbox: `Saya menyatakan bahwa apa yang saya isikan dalam form ini adalah benar adanya.`
- submit/save control
- existing entries table at the bottom

## Current working defaults

Use these unless the user says otherwise:

- `Jam Mulai`: `07:30`
- `Jam Selesai`: `16:00`
- choose `Tidak` for course-alignment
- tick the declaration checkbox before submit

## Activity synthesis rules

1. Gather same-day commits from both GitHub and GitLab.
2. Group them into a small number of real work themes.
3. Write one concise Indonesian summary suitable for an MIS daily logbook entry.
4. Prefer natural work language over raw commit fragments.
5. Do not fabricate work that is not supported by commits or other strong evidence.
6. Rewrite implementation notes if they contain literal SQL keywords or snippets.

## Submission checklist

1. Confirm the page is the KP entry form.
2. Scan the existing table first.
   - If an entry for today already exists, stop and decide whether to skip, replace, or ask before creating a duplicate.
3. Fill `Jam Mulai`, `Jam Selesai`, `Kegiatan/Materi`, `Tidak`, and the declaration checkbox.
4. Submit.
5. Verify `Simpan Data Berhasil` and the new row for today.
6. If the page also shows `Hapus Data Gagal` but the new row exists, treat it as page noise.

## Secret file format

The default MIS credentials file is a simple env file:

```bash
MIS_NETID=your-netid
MIS_PASSWORD=your-password
```

Keep that file outside the skill folder.

## Safety rules

- Never paste or repeat credentials into chat.
- Never store secrets in workspace notes or versioned skill files.
- Do not upload files unless the user explicitly asks.
- If commit data is missing or ambiguous, ask rather than inventing a fake summary.
