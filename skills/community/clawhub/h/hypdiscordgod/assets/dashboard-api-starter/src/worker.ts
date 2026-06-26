import 'dotenv/config';
import { getNextQueuedJob, markJobDone, markJobFailed, markJobRunning } from './jobs.js';

async function processJob(job: any) {
  console.log('Processing job', job.id, job.type, job.payload_json);
  // Replace with actual Discord/API side effects.
}

async function loop() {
  const job = getNextQueuedJob();
  if (!job) {
    setTimeout(loop, 2000);
    return;
  }

  try {
    markJobRunning(job.id);
    await processJob(job);
    markJobDone(job.id);
  } catch (error) {
    markJobFailed(job.id, error instanceof Error ? error.message : String(error));
  }

  setTimeout(loop, 250);
}

loop();
