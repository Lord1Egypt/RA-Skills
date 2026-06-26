import { FsStore } from '../storage/fs-store';
import { EventService } from '../control-plane/event-service';
import { RunService } from '../control-plane/run-service';
import { CheckpointService } from '../control-plane/checkpoint-service';
import { SessionService } from '../control-plane/session-service';
import { AttentionService } from '../control-plane/attention-service';
import { BindingService } from '../control-plane/binding-service';
import { ShareService } from '../control-plane/share-service';
import { SpoolService } from '../control-plane/spool-service';
import { ShadowService } from '../control-plane/shadow-service';
import { SkillTraceService } from '../telemetry/skill-trace';
import { CapabilityFactService } from '../telemetry/capability-facts';
import { buildCommandRegistry } from './commands';
import {
  isAutostartDisabled,
  isServerProcess,
  readManagerSettings,
  resolveBindHost,
  resolveSidecarBaseUrl,
} from './local-config';
import { checkSidecarHealth } from './sidecar-health';
import { launchSidecarProcess } from './sidecar-launcher';
import { updateAutostartConsent } from './autostart-consent';

const wait = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export interface SidecarStatus {
  status: 'running' | 'launched' | 'consent_required' | 'autostart_disabled' | 'launch_failed';
  reason: string | null;
  consent_required: boolean;
  launched: boolean;
  already_running: boolean;
  base_url: string;
  bind_host: string;
  next_steps: string[];
}

const baseSidecarStatus = () => ({
  base_url: resolveSidecarBaseUrl(),
  bind_host: resolveBindHost(),
});

const sidecarNextSteps = (status: SidecarStatus['status']) => {
  if (status === 'consent_required') {
    return [
      'Review the local-only sidecar behavior in SECURITY.md.',
      'Run "npm run consent:autostart" to allow future automatic startup.',
      'Or start the sidecar manually with "npm run dev".',
    ];
  }

  if (status === 'autostart_disabled' || status === 'launch_failed') {
    return [
      'Start the loopback-only sidecar manually with "npm run dev".',
      'Run "npm run consent:autostart" if you want future bootstrap runs to auto-start the sidecar.',
    ];
  }

  return [];
};

export const ensureSidecarRunning = async (): Promise<SidecarStatus> => {
  const store = new FsStore();
  await store.ensureLayout();

  if (await checkSidecarHealth()) {
    return {
      ...baseSidecarStatus(),
      status: 'running',
      reason: null,
      consent_required: false,
      launched: false,
      already_running: true,
      next_steps: [],
    };
  }

  if (isServerProcess()) {
    return {
      ...baseSidecarStatus(),
      status: 'autostart_disabled',
      reason: 'sidecar_process_bootstrap_skipped_inside_server',
      consent_required: false,
      launched: false,
      already_running: false,
      next_steps: sidecarNextSteps('autostart_disabled'),
    };
  }

  if (isAutostartDisabled()) {
    return {
      ...baseSidecarStatus(),
      status: 'autostart_disabled',
      reason: 'autostart_disabled_by_environment',
      consent_required: false,
      launched: false,
      already_running: false,
      next_steps: sidecarNextSteps('autostart_disabled'),
    };
  }

  const settings = await readManagerSettings(store);
  if (!settings.sidecar_autostart_consent) {
    return {
      ...baseSidecarStatus(),
      status: 'consent_required',
      reason: 'sidecar_autostart_not_confirmed',
      consent_required: true,
      launched: false,
      already_running: false,
      next_steps: sidecarNextSteps('consent_required'),
    };
  }

  await launchSidecarProcess();

  for (let attempt = 0; attempt < 10; attempt += 1) {
    if (await checkSidecarHealth()) {
      return {
        ...baseSidecarStatus(),
        status: 'launched',
        reason: null,
        consent_required: false,
        launched: true,
        already_running: false,
        next_steps: [],
      };
    }
    await wait(300);
  }

  return {
    ...baseSidecarStatus(),
    status: 'launch_failed',
    reason: 'sidecar_health_check_failed_after_launch',
    consent_required: false,
    launched: false,
    already_running: false,
    next_steps: sidecarNextSteps('launch_failed'),
  };
};

export const bootstrapManagerRuntime = async () => {
  const store = new FsStore();
  await store.ensureLayout();

  const eventService = new EventService(store);
  const runService = new RunService(store);
  const checkpointService = new CheckpointService(store);
  const spoolService = new SpoolService(store);
  const sessionService = new SessionService(store, runService, eventService, checkpointService, spoolService);
  const attentionService = new AttentionService(store);
  const bindingService = new BindingService(store);
  const shareService = new ShareService(store, eventService, runService, checkpointService, spoolService);
  const skillTraceService = new SkillTraceService(store, eventService);
  const capabilityFactService = new CapabilityFactService(store, eventService, skillTraceService);
  const shadowService = new ShadowService(
    store,
    sessionService,
    eventService,
    attentionService,
    bindingService,
    spoolService
  );

  return {
    store,
    eventService,
    runService,
    checkpointService,
    spoolService,
    sessionService,
    attentionService,
    bindingService,
    shareService,
    shadowService,
    skillTraceService,
    capabilityFactService,
    commands: buildCommandRegistry(
      sessionService,
      attentionService,
      bindingService,
      shareService,
      capabilityFactService,
      shadowService
    ),
  };
};

if (require.main === module) {
  (async () => {
    if (process.argv.includes('--allow-autostart')) {
      await updateAutostartConsent('allow', 'bootstrap_flag');
    } else if (process.argv.includes('--deny-autostart')) {
      await updateAutostartConsent('deny', 'bootstrap_flag');
    }

    const sidecar = await ensureSidecarRunning();
    const runtime = await bootstrapManagerRuntime();
    process.stdout.write(
      `${JSON.stringify(
        {
          product: 'openclaw-manager',
          state_root: runtime.store.rootDir,
          sidecar,
          commands: Object.keys(runtime.commands),
        },
        null,
        2
      )}\n`
    );
  })().catch((error) => {
    console.error(error);
    process.exit(1);
  });
}
