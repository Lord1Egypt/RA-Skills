# kn CLI

## Contents

- [Install](#install)
- [Service lifecycle](#service-lifecycle)
- [Environment, resources, and probes](#environment-resources-and-probes)
- [Autoscaling](#autoscaling)
- [Revisions and traffic](#revisions-and-traffic)
- [Domains](#domains)
- [Debugging with kn](#debugging-with-kn)

`kn` is the ergonomic CLI for creating and operating Knative resources. It does not install Knative Serving or Eventing.

## Install

Use one of the official install paths:

```bash
brew install knative/client/kn
```

Or download the matching binary from the Knative client GitHub releases, rename it to `kn`, make it executable, and place it on `PATH`:

```bash
mv <downloaded-kn-binary> kn
chmod +x kn
mv kn /usr/local/bin
kn version
```

For temporary use, run the official container image with kubeconfig mounted:

```bash
docker run --rm -v "$HOME/.kube/config:/root/.kube/config" gcr.io/knative-releases/knative.dev/client/cmd/kn:latest service list
```

## Service lifecycle

Create:

```bash
kn service create hello \
  --image ghcr.io/knative/helloworld-go:latest \
  --port 8080 \
  --env TARGET=World \
  -n default
```

Update, creating a new Revision:

```bash
kn service update hello \
  --image ghcr.io/example/app:v2 \
  --env TARGET=Knative \
  -n default
```

Describe and get URL:

```bash
kn service list -n default
kn service describe hello -n default
kn service describe hello -n default -o url
```

Delete:

```bash
kn service delete hello -n default
```

## Environment, resources, and probes

Common operational flags:

```bash
kn service update hello --env KEY=value -n default
kn service update hello --env KEY- -n default
kn service update hello --request cpu=250m,memory=256Mi --limit cpu=1,memory=512Mi -n default
kn service update hello --port 8080 -n default
```

For complex probes, volumes, multiple containers, securityContext, or nontrivial resources, prefer YAML because it is clearer and reviewable.

## Autoscaling

Set common annotations through `kn`:

```bash
kn service update hello \
  --annotation autoscaling.knative.dev/min-scale=1 \
  --annotation autoscaling.knative.dev/max-scale=10 \
  --annotation autoscaling.knative.dev/metric=concurrency \
  --annotation autoscaling.knative.dev/target=50 \
  -n default
```

If a `kn` version supports dedicated autoscale flags, they are fine for interactive operations, but YAML is safer for reproducible production configuration.

## Revisions and traffic

List Revisions:

```bash
kn revisions list -n default
kn revision describe hello-00002 -n default
```

Split traffic:

```bash
kn service update hello \
  --traffic hello-00001=10 \
  --traffic @latest=90 \
  -n default
```

Tag Revisions to create stable tag URLs:

```bash
kn service update hello \
  --tag hello-00001=stable \
  --tag @latest=canary \
  -n default
```

Rollback to a Revision:

```bash
kn service update hello --traffic hello-00001=100 -n default
```

## Debugging with kn

```bash
kn service describe hello -n default
kn route describe hello -n default
kn revisions list -n default
kn revision describe <revision> -n default
```

Use `kubectl` when you need generated resources, events, raw status conditions, CRD schemas, or controller logs.
