# Archetype: SLURM cluster

For HPC-style clusters with a controller node (`slurmctld`) and one or more compute nodes (`slurmd`).

## When to use this archetype

- Beowulf-style cluster with SLURM workload manager
- Head node runs `slurmctld`, compute nodes run `slurmd`
- Cluster filesystem shared via NFS

## YAML — head node

```yaml
- name: cluster-head
  address: 192.0.2.60
  auth: ssh-pass
  user: admin
  password_env: HEARTH_PASS_CLUSTER
  services: [ssh, slurmctld, slurmd, munge, nfs-mountd]
  apps:
    - name: slurm-status
      type: command
      command: 'sinfo -h -o "%n=%T" | sort -u | tr "\n" " "'
      expect_no_match: '(down|drain)'
```

## YAML — compute node

```yaml
- name: cluster-compute-01
  address: 192.0.2.61
  auth: ssh-pass
  user: admin
  password_env: HEARTH_PASS_CLUSTER
  services: [ssh, slurmd, munge]
  expected_failed_units: [lightdm, plymouth-quit]   # headless, expected to fail
  apps:
    - name: nfs-mount-shared
      type: command
      command: 'timeout 3 ls /cluster/shared >/dev/null 2>&1 && echo ok || echo FAIL'
      expect_match: '^ok$'
    - name: nfs-mount-home
      type: command
      command: 'timeout 3 ls /cluster/home >/dev/null 2>&1 && echo ok || echo FAIL'
      expect_match: '^ok$'
```

## What the 5 layers will show

Head:
```
=== 192.0.2.60 cluster-head ===
  L1 ping:    OK
  L2 uptime:  3 weeks, 5 days, load: 0.00 0.01 0.00
  L3 mem:     used 1.1Gi / 7.6Gi, 6.5Gi avail | disk: / 4% used, 208G free
  L4 svc:     ssh=active slurmctld=active slurmd=active munge=active nfs-mountd=active
  L5 app:     slurm-status=OK (cluster-head=idle compute-01=idle)
```

Compute:
```
=== 192.0.2.61 cluster-compute-01 ===
  L1 ping:    OK
  L2 uptime:  3 weeks, 5 days, load: 0.00 0.00 0.00
  L3 mem:     used 530Mi / 3.8Gi, 3.2Gi avail | disk: / 3% used, 212G free
  L4 svc:     ssh=active slurmd=active munge=active
  L5 app:     nfs-mount-shared=OK (ok) | nfs-mount-home=OK (ok)
```

## Why probe NFS mount health on compute nodes?

If `cluster-head` reboots or NFS hiccups, the compute nodes' mounts can go stale before SLURM notices. The `timeout 3 ls /cluster/shared` probe catches a stale mount in 3 seconds without hanging.

## Why probe `sinfo` on the head?

If `compute-01` shows `down*` or `drain` in `sinfo`, the cluster can't run jobs even though everything else looks fine. Common cause: munge-key mismatch between head and compute. The `expect_no_match: '(down|drain)'` clause flips L5 to a failure if either appears.

## Tweaks

- **Multiple compute nodes**: copy the compute block, change `name` and `address`. Add them to a `groups: cluster:` list for fast partial sweeps.
- **GPU compute nodes**: add `nvidia-persistenced` or `nvidia-fabricmanager` to `services:`.
- **MPI installation health**: add an L5 command probe for `mpirun --version` or a quick MPI-hello-world.