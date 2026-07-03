# 1. Postgres migration plan

1. **Prepare the new server and copy the data**
   Set up the new server, install the same Postgres version, and take a full copy of the current database.

2. **Test the copied data in a safe environment**
   Load the copy onto a test server and confirm everything (tables, user accounts, settings) is intact.

3. **Plan and run the cutover**
   Pick a low-traffic window, stop writes on the old server, apply the latest changes to the new server, and switch the app over.

4. **Verify and monitor after the switch**
   Watch the new server for errors, slow queries, and missing data during the first hours and days.

5. **Clean up and document**
   Once the new server is stable, remove the old one and write down what was done for the team.

---

# 2. Upload error

**The upload didn't go through.**

I tried to read the file at `/tmp/profile.jpg`, but that file doesn't exist on the server, so the upload failed.

**What this means:** the file was never received, or it was saved somewhere other than `/tmp`.

**What to do next:** please try uploading the file again. If it keeps failing, let me know the file name and roughly when you uploaded it, and I'll look into where it went.

---

# 3. CSV processing status

**Start:**
> Processing your file (`data.csv`, 10,000 rows). This usually takes a few minutes. I'll show you progress as I go.

**Middle:**
> About halfway through — 5,000 of 10,000 rows done. No errors so far. Keep going.

**End:**
> Done. All 10,000 rows were processed successfully. The results are ready to use.
