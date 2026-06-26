import os
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("MooTeamClient")

class MooTeamClient:
    def __init__(self):
        self.base_url = "https://api.moo.team/api"
        self.token = os.getenv("MOOTEAM_API_TOKEN")
        self.company = os.getenv("MOOTEAM_COMPANY_ALIAS")
        
        if not self.token or not self.company:
            logger.error("Отсутствуют переменные окружения MOOTEAM_API_TOKEN или MOOTEAM_COMPANY_ALIAS")
            raise EnvironmentError("Настройте окружение")

    @property
    def headers(self):
        return {
            "Authorization": f"Bearer {self.token}",
            "X-MT-Company": self.company,
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def _request(self, method, endpoint, params=None, data=None):
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        try:
            response = requests.request(
                method=method, url=url, headers=self.headers, params=params, json=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            return {"error": True, "status": response.status_code, "message": response.text}
        except Exception as e:
            return {"error": True, "message": str(e)}

    # --- PROJECTS & TEAMS ---
    def get_projects(self):
        return self._request("GET", "/projects")

    def create_project(self, name, workflow_id, **kwargs):
        data = {"name": name, "workflowId": workflow_id}
        data.update(kwargs)
        return self._request("POST", "/projects", data=data)

    def get_project_details(self, project_id):
        return self._request("GET", f"/projects/{project_id}")

    def update_project(self, project_id, data):
        return self._request("PUT", f"/projects/{project_id}", data=data)

    def delete_project(self, project_id):
        return self._request("DELETE", f"/projects/{project_id}")

    def add_team_member(self, project_id, user_id):
        return self._request("POST", "/project-team-maps", data={"projectId": project_id, "userId": user_id})

    def remove_team_member(self, map_id):
        return self._request("DELETE", f"/project-team-maps/{map_id}")

    def get_user_profiles(self):
        return self._request("GET", "/user-profiles")

    # --- TASKS & DRAFTS ---
    def get_tasks(self, project_id=None):
        params = {"projectId": project_id} if project_id else {}
        return self._request("GET", "/tasks", params=params)

    def create_task(self, project_id, header, **kwargs):
        data = {"projectId": project_id, "header": header}
        data.update(kwargs)
        return self._request("POST", "/tasks", data=data)

    def get_task_details(self, task_id):
        return self._request("GET", f"/tasks/{task_id}")

    def update_task(self, task_id, data):
        return self._request("PUT", f"/tasks/{task_id}", data=data)

    def delete_task(self, task_id):
        return self._request("DELETE", f"/tasks/{task_id}")

    def get_task_draft(self):
        return self._request("GET", "/task-drafts/current")

    def update_task_draft(self, data):
        return self._request("PUT", "/task-drafts/current", data=data)

    def create_task_from_draft(self):
        return self._request("POST", "/task-drafts/create-task")

    # --- COMMENTS ---
    def get_comments(self, task_id):
        return self._request("GET", "/task-comments", params={"taskId": task_id})

    def create_comment(self, task_id, text):
        return self._request("POST", "/task-comments", data={"taskId": task_id, "text": text})

    def delete_comment(self, comment_id):
        return self._request("DELETE", f"/task-comments/{comment_id}")

    # --- LABELS ---
    def get_label_groups(self):
        return self._request("GET", "/task-label-groups")

    def create_label_group(self, name):
        return self._request("POST", "/task-label-groups", data={"name": name})

    def update_label_group(self, group_id, name):
        return self._request("PUT", f"/task-label-groups/{group_id}", data={"name": name})

    def delete_label_group(self, group_id):
        return self._request("DELETE", f"/task-label-groups/{group_id}")

    def get_labels(self):
        return self._request("GET", "/task-labels")

    def get_label_details(self, label_id):
        return self._request("GET", f"/task-labels/{label_id}")

    def create_label(self, group_id, name, color="#673ab7"):
        data = {"labelGroupId": group_id, "name": name, "color": color or "#673ab7"}
        return self._request("POST", "/task-labels", data=data)

    def update_label(self, label_id, data):
        return self._request("PUT", f"/task-labels/{label_id}", data=data)

    def delete_label(self, label_id):
        return self._request("DELETE", f"/task-labels/{label_id}")

    # --- TIMER & TIME LOGS ---
    def start_timer(self, task_id):
        return self._request("POST", "/timer/start", data={"taskId": task_id})

    def stop_timer(self):
        return self._request("POST", "/timer/stop")

    def get_timer_current(self):
        return self._request("GET", "/timer/current")

    def get_task_time_list(self, task_id):
        return self._request("GET", f"/timer/task-time-list/{task_id}")

    def get_time_logs(self):
        return self._request("GET", "/timer/time-logs")

    def create_time_log(self, task_id, seconds):
        return self._request("POST", "/timer/time-logs", data={"taskId": task_id, "seconds": seconds})

    def update_time_log(self, log_id, seconds):
        return self._request("PUT", f"/timer/time-logs/{log_id}", data={"seconds": seconds})

    def delete_time_log(self, log_id):
        return self._request("DELETE", f"/timer/time-logs/{log_id}")

    # --- DICTIONARIES & LOGS ---
    def get_workflows(self):
        return self._request("GET", "/task-workflows")

    def create_workflow(self, name):
        return self._request("POST", "/task-workflows", data={"name": name})

    def get_workflow_details(self, workflow_id):
        return self._request("GET", f"/task-workflows/{workflow_id}")

    def update_workflow(self, workflow_id, name):
        return self._request("PUT", f"/task-workflows/{workflow_id}", data={"name": name})

    def delete_workflow(self, workflow_id):
        return self._request("DELETE", f"/task-workflows/{workflow_id}")

    def get_statuses(self, workflow_id=None):
        params = {"workflowId": workflow_id} if workflow_id else {}
        return self._request("GET", "/task-statuses", params=params)

    def create_status(self, name, workflow_id):
        return self._request("POST", "/task-statuses", data={"name": name, "workflowId": workflow_id})

    def get_status_details(self, status_id):
        return self._request("GET", f"/task-statuses/{status_id}")

    def update_status(self, status_id, name):
        return self._request("PUT", f"/task-statuses/{status_id}", data={"name": name})

    def delete_status(self, status_id):
        return self._request("DELETE", f"/task-statuses/{status_id}")

    def get_activity_logs(self, project_id=None, user_id=None, type_name=None):
        params = {}
        if project_id: params["projectId"] = project_id
        if user_id: params["userId"] = user_id
        if type_name: params["type"] = type_name
        return self._request("GET", "/activity-logs", params=params)

    def get_activity_projects(self):
        return self._request("GET", "/activity-logs/project-list")