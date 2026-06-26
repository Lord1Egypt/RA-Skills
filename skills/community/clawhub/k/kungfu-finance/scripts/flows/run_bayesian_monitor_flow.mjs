import {
  assertBayesianMonitorAction,
  buildBayesianMonitorRequest,
  isMain,
  parseCommonArgs,
  runCli
} from "../core/cli.mjs";
import { getOpenKey } from "../core/runtime.mjs";
import { getBayesianMonitorTaskRecords } from "../products/bayesian_monitor_records.mjs";
import { getBayesianMonitorTasks } from "../products/bayesian_monitor_tasks.mjs";

const DEFAULT_RECORD_LIMIT = 5;

function buildNeedsInputResponse({
  action,
  prompt,
  missing,
  reason,
  options,
  attempted
}) {
  return {
    action,
    status: "needs_input",
    prompt,
    missing,
    reason,
    ...(options ? { options } : {}),
    ...(attempted ? { attempted } : {})
  };
}

function buildBlockedResponse({ action, reason, message }) {
  return {
    action,
    status: "blocked",
    reason,
    message
  };
}

function normalizeTaskSummary(item) {
  return {
    task_id: item.task_id,
    topic: item.topic,
    topic_type: item.topic_type,
    period: item.period,
    original_report_date: item.original_report_date,
    direction: item.parsed?.direction ?? null,
    confidence: item.parsed?.confidence ?? null,
    core_logic: item.parsed?.core_logic ?? null,
    auto_update: item.auto_update,
    created_at: item.created_at,
    updated_at: item.updated_at
  };
}

function normalizeRecord(item) {
  return {
    monitor_date: item.monitor_date,
    topic: item.topic,
    direction: item.direction,
    confidence: item.confidence,
    core_logic: item.core_logic,
    is_changed: item.is_changed,
    change_type: item.change_type,
    change_reason: item.change_reason,
    content: item.content,
    created_at: item.created_at
  };
}

async function loadTasks() {
  const payload = await getBayesianMonitorTasks();
  return Array.isArray(payload?.data) ? payload.data : [];
}

function buildTaskOptions(tasks) {
  return {
    tasks: tasks.map(normalizeTaskSummary)
  };
}

function resolveTaskBySelector(tasks, request) {
  const hasTaskId = Boolean(request.bayesian_task_id);
  const hasTopic = Boolean(request.bayesian_topic);

  if (hasTaskId && hasTopic) {
    return {
      response: buildNeedsInputResponse({
        action: "reports",
        missing: ["task"],
        reason: "ambiguous_task_selector",
        prompt: "请只提供一个监控任务标识。你可以使用 bayesian-task-id 或 bayesian-topic 其一重新查询。",
        options: buildTaskOptions(tasks),
        attempted: {
          bayesian_task_id: request.bayesian_task_id,
          bayesian_topic: request.bayesian_topic
        }
      })
    };
  }

  if (!hasTaskId && !hasTopic) {
    return {
      response: buildNeedsInputResponse({
        action: "reports",
        missing: ["task"],
        reason: "missing_task",
        prompt: "请先选择一个贝叶斯监控任务。",
        options: buildTaskOptions(tasks)
      })
    };
  }

  if (hasTaskId) {
    const matchedById = tasks.find((item) => item.task_id === request.bayesian_task_id);
    if (!matchedById) {
      return {
        response: buildNeedsInputResponse({
          action: "reports",
          missing: ["task"],
          reason: "task_not_found",
          prompt: "未找到这个贝叶斯监控任务，请从当前任务列表中重新选择。",
          options: buildTaskOptions(tasks),
          attempted: {
            bayesian_task_id: request.bayesian_task_id
          }
        })
      };
    }

    return { task: matchedById };
  }

  const targetTopic = request.bayesian_topic.trim();
  const matchedByTopic = tasks.filter((item) => item.topic === targetTopic);

  if (matchedByTopic.length === 0) {
    return {
      response: buildNeedsInputResponse({
        action: "reports",
        missing: ["task"],
        reason: "task_not_found",
        prompt: "未找到这个贝叶斯监控主题，请从当前任务列表中重新选择。",
        options: buildTaskOptions(tasks),
        attempted: {
          bayesian_topic: targetTopic
        }
      })
    };
  }

  if (matchedByTopic.length > 1) {
    return {
      response: buildNeedsInputResponse({
        action: "reports",
        missing: ["task"],
        reason: "task_ambiguous",
        prompt: "存在同名贝叶斯监控任务，请改用 bayesian-task-id 重新选择。",
        options: buildTaskOptions(matchedByTopic),
        attempted: {
          bayesian_topic: targetTopic
        }
      })
    };
  }

  return { task: matchedByTopic[0] };
}

async function listBayesianMonitorFlow() {
  const tasks = await loadTasks();

  return {
    action: "list",
    status: "completed",
    tasks: tasks.map(normalizeTaskSummary),
    total: tasks.length,
    ...(tasks.length === 0
      ? { message: "当前账号下还没有贝叶斯监控任务。" }
      : {})
  };
}

async function reportsBayesianMonitorFlow(request) {
  const tasks = await loadTasks();

  if (tasks.length === 0) {
    return buildBlockedResponse({
      action: "reports",
      reason: "empty_task_list",
      message: "当前账号下还没有可查询的贝叶斯监控任务。"
    });
  }

  const selection = resolveTaskBySelector(tasks, request);
  if (selection.response) {
    return selection.response;
  }

  const task = selection.task;
  const limit = request.bayesian_record_limit ?? DEFAULT_RECORD_LIMIT;
  const recordPayload = await getBayesianMonitorTaskRecords({
    task_id: task.task_id,
    limit
  });

  return {
    action: "reports",
    status: "completed",
    task: normalizeTaskSummary(task),
    initial_report: task.original_report,
    records: Array.isArray(recordPayload?.data) ? recordPayload.data.map(normalizeRecord) : [],
    record_limit: limit
  };
}

export async function runBayesianMonitorFlow(values) {
  getOpenKey();
  const request = buildBayesianMonitorRequest(values);
  assertBayesianMonitorAction(request);

  if (request.bayesian_action === "list") {
    return listBayesianMonitorFlow();
  }

  if (request.bayesian_action === "reports") {
    return reportsBayesianMonitorFlow(request);
  }

  throw new Error("不支持的贝叶斯监控动作。");
}

if (isMain(import.meta)) {
  await runCli(async () => {
    const { values } = parseCommonArgs();
    return runBayesianMonitorFlow(values);
  });
}
