import sys

def main():
    argv = sys.argv[1:]
    wants_audit = "--audit" in argv

    has_positional_target = any(a for a in argv if a and not a.startswith("-"))
    has_targets_file = "--targets-file" in argv
    has_targets = has_positional_target or has_targets_file

    if wants_audit and not has_targets:
        import run_audit

        run_audit.main()
        return

    import run_scan

    run_scan.main()

if __name__ == "__main__":
    main()
