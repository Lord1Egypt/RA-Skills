#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Inspect an ncps wiring structure (layer sizes, synapse counts, graph image).

Examples:
  python inspect_wiring.py --type autoncp --units 28 --output-size 4 --input-size 20
  python inspect_wiring.py --type autoncp --units 28 --output-size 4 --draw wiring.png
  python inspect_wiring.py --type fc --units 16
"""

import argparse


def build_parser():
    p = argparse.ArgumentParser(
        prog="inspect_wiring.py",
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--type", choices=["autoncp", "ncp", "random", "fc"],
                   default="autoncp", help="wiring class to inspect (default autoncp)")
    p.add_argument("--units", type=int, default=28,
                   help="total neurons / hidden units (default 28)")
    p.add_argument("--output-size", type=int, default=4,
                   help="number of motor neurons / outputs (default 4)")
    p.add_argument("--input-size", type=int, default=20,
                   help="input dimension (sensory neurons, default 20)")
    p.add_argument("--sparsity", type=float, default=0.5,
                   help="sparsity for autoncp/random: 0.0 .. 0.9 (default 0.5)")
    p.add_argument("--seed", type=int, default=22222,
                   help="wiring random seed (default 22222, matches ncps default)")
    p.add_argument("--draw", default=None,
                   help="save the wiring graph to a PNG file (requires matplotlib)")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)

    try:
        from ncps.wirings import AutoNCP, FullyConnected, NCP, Random
    except ImportError:
        import sys
        sys.exit("ncps is not installed. Run: pip install -r scripts/requirements.txt")

    if args.type == "autoncp":
        w = AutoNCP(args.units, args.output_size, sparsity_level=args.sparsity,
                    seed=args.seed)
        state_size = args.units
    elif args.type == "random":
        w = Random(args.units, args.output_size, sparsity_level=args.sparsity,
                   random_seed=args.seed)
        state_size = args.units
    elif args.type == "fc":
        w = FullyConnected(args.units)
        state_size = args.units
    else:  # explicit 4-layer NCP
        inter = max(args.units - args.output_size - 4, 4)
        w = NCP(inter_neurons=inter, command_neurons=4,
                motor_neurons=args.output_size, sensory_fanout=6,
                inter_fanout=4, recurrent_command_synapses=4,
                motor_fanin=6, seed=args.seed)
        state_size = inter + 4 + args.output_size

    try:
        w.set_input_dim(args.input_size)
        layers = w.num_layers
    except Exception:
        layers = None

    print(f"Wiring: {args.type}")
    print(f"  input size (sensory): {args.input_size}")
    print(f"  state size (total neurons): {state_size}")
    print(f"  output size (motor): {args.output_size}")
    if layers is not None:
        print(f"  layers: {layers}")
        for i in range(layers):
            try:
                n = len(w.get_neurons_of_layer(i))
            except Exception:
                n = "?"
            print(f"    layer {i}: {n} neurons")
    try:
        print(f"  internal synapses: {w.synapse_count}")
    except Exception:
        print("  internal synapses: (needs build)")
    try:
        print(f"  sensory synapses: {w.sensory_synapse_count}")
    except Exception:
        print("  sensory synapses: (needs build)")

    if args.draw:
        try:
            import matplotlib
            matplotlib.use("Agg")
            import matplotlib.pyplot as plt
        except ImportError:
            print("matplotlib is not installed; skipping graph rendering")
            return
        try:
            import matplotlib.pyplot as plt
            legend_handles = w.draw_graph(draw_labels=True)
            plt.legend(handles=legend_handles, loc="upper center",
                       bbox_to_anchor=(0.5, 1.02), ncol=3)
            plt.tight_layout()
            plt.savefig(args.draw, dpi=150)
            print(f"Wiring graph saved to: {args.draw}")
        except Exception as exc:
            print(f"Could not render the graph: {exc}")


if __name__ == "__main__":
    main()
