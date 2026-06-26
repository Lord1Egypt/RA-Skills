# GitOps 与 Harbor 集成

## Argo CD Image Updater

Argo CD Image Updater 可以自动监听 Harbor 并更新 Git 中的镜像版本。

### 安装 Argo CD Image Updater

```bash
kubectl apply -f https://raw.githubusercontent.com/argocd-image-updater/release-v0.12/manifests/install.yaml
```

### 配置 Harbor Registry

```bash
# 创建 Harbor Pull Secret
kubectl create secret docker-registry harbor-secret \
  --docker-server=https://harbor.mycompany.com \
  --docker-username=robot$my-app$argocd \
  --docker-password=$ROBOT_TOKEN \
  -n argocd

# ArgoCD 集群注册（可选，用于跨集群部署）
argocd cluster add in-cluster --current-context
```

### ArgoCD Application 配置

```yaml
# app-my-app.yaml
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: my-app
  namespace: argocd
  annotations:
    argocd-image-updater.argoproj.io/image-list: my-app=harbor.mycompany.com/my-app/my-app--api
    argocd-image-updater.argoproj.io/my-app.update-strategy: latest
    argocd-image-updater.argoproj.io/my-app.helm.image-spec: |
      image.repository: harbor.mycompany.com/my-app/my-app--api
      image.tag: "{{.Tag}}"
spec:
  project: my-app
  source:
    repoURL: https://github.com/myorg/my-app-gitops.git
    targetRevision: main
    path: k8s/overlays/prod
  destination:
    server: https://kubernetes.default.svc
    namespace: my-app
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
```

### 配置 Webhook 自动更新

Argo CD Image Updater 支持轮询或 Webhook 触发：

```bash
# 在 Harbor 中配置 Webhook
# 地址: https://argocd-image-updater.mycompany.com/webhook/harbor
# 事件: PUSH_ARTIFACT

# 或使用轮询（每5分钟）
argocd-image-updater.argoproj.io/image-list: my-app=harbor.mycompany.com/my-app/my-app--api
argocd-image-updater.argoproj.io/my-app.update-strategy: latest
argocd-image-updater.argoproj.io/my-app.pull-secret: pullsecret:argocd/harbor-secret
argocd-image-updater.argoproj.io/my-app.force-update: "true"
```

## Flux CD (v2)

Flux 可以自动同步 Harbor 镜像变更。

### Flux ImagePolicy + ImageUpdateAutomation

```yaml
# image-policy.yaml
apiVersion: image.toolkit.fluxcd.io/v1beta1
kind: ImagePolicy
metadata:
  name: my-app
  namespace: my-app
spec:
  imageRepositoryRef:
    name: my-app-api
    namespace: my-app
  policy:
    semver:
      range: ">=1.0.0"
    # 或使用 latest
    alphabetical:
      order: asc

---
# image-repository.yaml
apiVersion: image.toolkit.fluxcd.io/v1beta1
kind: ImageRepository
metadata:
  name: my-app-api
  namespace: my-app
spec:
  image: harbor.mycompany.com/my-app/my-app--api
  secretRef:
    name: harbor-credentials
  interval: 5m

---
# image-update-automation.yaml
apiVersion: image.toolkit.fluxcd.io/v1beta1
kind: ImageUpdateAutomation
metadata:
  name: my-app-gitops
  namespace: my-app
spec:
  sourceRef:
    kind: GitRepository
    name: my-app-gitops
  git:
    checkout:
      ref:
        branch: main
    commit:
      author:
        email: flux@mycompany.com
        name: flux-bot
    push:
      branch: main
  update:
    path: ./k8s
    strategy: Setters
```

### 在 K8s YAML 中声明镜像版本

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: my-app
spec:
  template:
    spec:
      containers:
        - name: my-app
          image: harbor.mycompany.com/my-app/my-app--api:latest # 会被自动更新
          # flux 会自动更新此处的 tag
```

Flux 会在检测到新镜像后，自动提交 Git：

```diff
- image: harbor.mycompany.com/my-app/my-app--api:v1.2.2
+ image: harbor.mycompany.com/my-app/my-app--api:v1.2.3
```

## Helm + GitOps

### 用 Helm 管理 Harbor 项目配置

```yaml
# helm/harbor-projects/values.yaml
projects:
  - name: my-app
    description: "业务镜像仓库"
    storageQuota: 500G
    public: false
    autoScan: true
    preventVulnerableImages: true
    severityThreshold: high
    retentionPolicies:
      - name: keep-releases
        rule: keep_last_n
        params:
          n: 5
        scope: "**"

  - name: proxy-cache-dockerhub
    description: "Docker Hub 代理缓存"
    proxyCache: true
    public: false
```

### Helm 模板生成 Harbor 配置

```bash
helm template harbor-projects ./helm/harbor-projects | \
  kubectl apply -f -
```

## 声明式管理复制规则

```yaml
# replication-rules.yaml（可用于 Flux Terraform 等工具）
apiVersion: v1
kind: ConfigMap
metadata:
  name: harbor-replication-rules
  namespace: harbor
data:
  rules: |
    - name: prod-to-dr
      src_registry: local
      dest_registry:
        url: https://harbor-dr.mycompany.com
        credential: harbor-dr-secret
      filters:
        - type: name
          value: "prod/.*"
        - type: tag
          value: ".*"
      trigger:
        type: scheduled
        cron: "0 0 2 * * *"
      deletion: true
      override: true
```

## CI/CD 流水线示例

### GitLab CI

```yaml
# .gitlab-ci.yml
variables:
  HARBOR_URL: harbor.mycompany.com
  PROJECT: my-app
  IMAGE: $HARBOR_URL/$PROJECT/my-app--api

build:
  stage: build
  image: docker:24-dind
  services:
    - docker:24-dind
  script:
    - |
      echo "$HARBOR_ROBOT_SECRET" | docker login -u "robot\$$PROJECT\$ci" --password-stdin $HARBOR_URL
    - docker build -t $IMAGE:$CI_COMMIT_SHORT_SHA .
    - docker push $IMAGE:$CI_COMMIT_SHORT_SHA
    # 添加版本标签
    - docker tag $IMAGE:$CI_COMMIT_SHORT_SHA $IMAGE:v${CI_COMMIT_BRANCH##release-}
    - docker push $IMAGE:v${CI_COMMIT_BRANCH##release-}

security_scan:
  stage: test
  image: aquasec/trivy:latest
  script:
    - trivy image --exit-code 1 --severity HIGH,CRITICAL $IMAGE:$CI_COMMIT_SHORT_SHA
  needs: [build]

deploy:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    # Argo CD 自动检测到新镜像并部署
    - kubectl set image deployment/my-app my-app=$IMAGE:$CI_COMMIT_SHORT_SHA -n my-app
  environment:
    name: production
  when: manual
  needs: [security_scan]
```

### GitHub Actions

```yaml
# .github/workflows/build.yml
name: Build and Push

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Login to Harbor
        uses: docker/login-action@v3
        with:
          registry: harbor.mycompany.com
          username: ${{ secrets.HARBOR_ROBOT_USER }}
          password: ${{ secrets.HARBOR_ROBOT_TOKEN }}

      - name: Build and Push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            harbor.mycompany.com/my-app/my-app--api:${{ github.sha }}
            harbor.mycompany.com/my-app/my-app--api:latest
          cache-from: type=registry,ref=harbor.mycompany.com/my-app/my-app--api:latest
          cache-to: type=inline
```
